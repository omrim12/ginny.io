import json
from datetime import date
from keras.models import save_model, load_model
from constants import (
    GENIE_NET_FNAME,
    GENIE_SCORE_FNAME
)


def save_genie(genie_model, loss, acc, food_types):
    save_model(
        genie_model,
        GENIE_NET_FNAME,
        overwrite=True,
        include_optimizer=True,
        save_format=None,
        signatures=None,
        options=None,
        save_traces=True
    )

    # save model loss, accuracy
    with open(GENIE_SCORE_FNAME, 'w') as net_meta_file:
        net_metadata = {
            'accuracy': acc,
            'loss': loss,
            'supported_food_types': food_types,
            'date': date.today()
        }
        json.dump(net_metadata, net_meta_file)


def load_genie():
    return load_model(GENIE_NET_FNAME)
