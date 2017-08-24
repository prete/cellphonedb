import os

import pandas as pd

from cellcommdb.api import current_dir
from cellcommdb.blend import Blend
from cellcommdb.extensions import db
from cellcommdb.models import Interaction
from cellcommdb.tools import filters, database


def load(interaction_file=None):
    if not interaction_file:
        interaction_file = os.path.join(current_dir, 'data', 'inweb_clean_columns.csv')

    csv_interaction_df = pd.read_csv(interaction_file, quotechar='"', na_values="-")

    interaction_df = Blend.blend_multidata(csv_interaction_df, ['protein_uniprot_1_id', 'protein_uniprot_2_id'])

    filters.remove_not_defined_columns(interaction_df, database.get_column_table_names(Interaction, db))

    interaction_df.to_sql(name='interaction', if_exists='append', con=db.engine, index=False)
