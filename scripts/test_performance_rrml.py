import asyncio
import pathlib
import time

import aiohttp
import joblib
import mwapi  # type: ignore
import pandas as pd  # type: ignore
from knowledge_integrity.models.revertrisk_multilingual import (classify,
                                                                load_model)
from knowledge_integrity.revision import get_current_revision
from tqdm import tqdm

model_path = 'pretrained_models/multilingual_revertrisk_model_v4.pkl'
model = load_model(pathlib.Path(model_path))

loop = asyncio.get_event_loop()


# getting session:
async def create_session():
    return aiohttp.ClientSession()
s = asyncio.get_event_loop().run_until_complete(create_session())


async def get_features(revision_id, lang, s=s):
    start = time.time()
    try:
        inputs = {"lang": lang, "rev_id": revision_id}
        lang = inputs.get("lang")
        rev_id = inputs.get("rev_id")

        session = mwapi.AsyncSession(
            f"https://{lang}.wikipedia.org",
            user_agent="Revision integrity inference feature extractor test",
            session=s,
        )
        rev = await get_current_revision(session, rev_id, lang)
        res = classify(model, rev)
        error = None
    except Exception as e:
        print(e)
        res = None
        error = e
    return revision_id, res, time.time() - start, error


df_sample = pd.read_csv("data/test_all_users_sample.csv")
revision_ids = df_sample.revision_id.values
langs = df_sample.wiki_db.apply(lambda x: x.replace("wiki", "")).values

batch_size = 20

all_results = []
print("Number of samples to process: ",  len(df_sample))
for i in tqdm(range(0, len(revision_ids), batch_size)):
    # more logic here
    tasks = [
        get_features(int(rev_id), lang)
        for rev_id, lang
        in zip(revision_ids[i:i+batch_size], langs[i:i+batch_size])
    ]
    res = loop.run_until_complete(asyncio.gather(*tasks))
    all_results += res

print(len(all_results))
filename = 'data/RRML_results.data'
joblib.dump(all_results, filename, compress=9)
