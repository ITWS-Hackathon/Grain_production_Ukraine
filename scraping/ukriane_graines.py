#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ukraine Datathon

# Cleaning csv/tsv file using pandas

import numpy as np
import pandas as pd


df = pd.read_csv('Ukraine_arableLand.csv')

df_ukraine = df[df['Country Name'] == 'Ukraine']

# df_ukraine.to_csv('psd_graines_Ukraine.csv', index=False)

columns = list(range(1960, 1992))
columns = [str(col) for col in columns]
df.drop(columns=columns, inplace=True)
df_trans = df.T

df_trans.to_csv('Ukraine_arableLand_cleanData2.csv')

