#!/usr/bin/env python3

import copy, itertools

import numpy as np
import pandas as pd
import igraph


def merge_info_df(df, id_map, merge_fn):

    to_drop = []
    new_rows = {}
    indices = set([])

    for (k,v) in id_map.items():
        if k == v:
            continue

        if v in new_rows:
            row_v = new_rows[v]
        else:
            row_v = df.loc[v]

        new_rows[v] = merge_fn(df.loc[k], row_v)

        to_drop.append(k)
        indices.add(v)

    index = sorted(list(indices))
    replacements = pd.DataFrame.from_dict(new_rows, orient="index")

    # indexing by columns ensures that they have the same order
    df.loc[index] = replacements[df.columns]
    df.drop(to_drop, inplace=True)

    return df


def empty_obj_array(shape):
    size = np.prod(shape)
    return np.array([None for _ in range(size)]).reshape(shape)


def find_connected_components(matches):

    all_ids = list(set(itertools.chain(*matches)))
    vertex_mapping = { segid: i for (i,segid) in enumerate(all_ids) }

    g = igraph.Graph(len(all_ids))
    g.vs["ids"] = all_ids

    mapped_edges = map(lambda x: (vertex_mapping[x[0]],vertex_mapping[x[1]]),
                       matches)

    g.add_edges(mapped_edges)

    vertex_ccs = g.components()

    orig_ccs = [g.vs[cc]["ids"] for cc in vertex_ccs]

    return orig_ccs


def make_id_map(ccs):

    mapping = {}

    for cc in ccs:
        target = min(cc)

        for i in cc:
            mapping[i] = target

    return mapping


def update_chunk_id_maps(chunk_id_maps, id_map):

    for mapping in chunk_id_maps.flat:
        for (k,v) in mapping.items():
            mapping[k] = id_map.get(v,v)

    return chunk_id_maps


def weighted_avg(com1, sz1, com2, sz2):

    frac1 = sz1 / (sz1+sz2)
    frac2 = sz2 / (sz1+sz2)

    h1 = (com1[0]*frac1, com1[1]*frac1, com1[2]*frac1)
    h2 = (com2[0]*frac2, com2[1]*frac2, com2[2]*frac2)

    return (h1[0]+h2[0], h1[1]+h2[1], h1[2]+h2[2])
