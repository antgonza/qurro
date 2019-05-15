#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# Copyright (c) 2018--, rankratioviz development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# ----------------------------------------------------------------------------

import logging
import pandas as pd


def read_metadata_file(md_file_loc):
    """Reads in a metadata file using pandas.read_csv().

       One slightly strange thing is that pandas.read_csv() interprets
       columns containing all values of True / False as booleans. This
       causes problems down the line, since these values are converted to
       true / false (note the lowercase) when using them in JavaScript.

       To ensure consistency with QIIME 2's metadata guidelines (which only
       consider numeric and categorical types), we convert all values in
       columns labelled with the bool type to strings. This preserves the
       "case" of True / False, and should result in predictable outcomes.
    """
    metadata_df = pd.read_csv(md_file_loc, index_col=0, sep="\t")

    bool_cols = metadata_df.select_dtypes(include=[bool]).columns
    if len(bool_cols) > 0:
        type_conv_dict = {col: str for col in bool_cols}
        metadata_df = metadata_df.astype(type_conv_dict)

    return metadata_df


def get_truncated_feature_id(full_feature_id):
    """Computes a truncated GNPS feature ID from a full GNPS feature ID.

       This function was originally contained in a Jupyter Notebook for
       processing this sort of data written by Jamie Morton and
       Julia Gauglitz.
    """
    mz, rt = list(map(float, full_feature_id.split(";")))
    return "{:.4f};{:.4f}".format(mz, rt)


def read_gnps_feature_metadata_file(md_file_loc, feature_ranks_df):
    """Reads in a GNPS feature metadata file, producing a sane DataFrame.

       Also requires a DataFrame describing feature ranks as input. This is so
       that we can match up the feature rank IDs in the ranks and BIOM table
       with rows in the GNPS metadata file -- the precision of the numbers from
       which GNPS feature IDs are computed varies between the ranks/BIOM table
       and the actual numbers contained in the GNPS metadata file.
    """
    # Note that we don't set index_col = 0 -- the columns we care about
    # ("parent mass", "RTConsensus", and "LibraryID"), as far as I know, don't
    # have a set position. So we'll just use the basic RangeIndex that pandas
    # defaults to.
    metadata_df = pd.read_csv(md_file_loc, sep="\t")

    # Create a feature ID column from the parent mass and RTConsensus cols.
    # Use of .map() here is derived from
    # https://stackoverflow.com/a/22276757/10730311.
    metadata_df["rankratioviz_trunc_feature_id"] = (
        metadata_df["parent mass"].map("{:.4f}".format)
        + ";"
        + metadata_df["RTConsensus"].map("{:.4f}".format)
    )

    # Go through feature rank index, and for each create a mapping of
    # (truncated feature ID) -> (full feature ID). Then use that mapping to
    # create a new column of "rankratioviz_full_feature_id" in metadata_df.
    # NOTE that if there are indistinguishable truncated IDs, this will raise
    # an error.
    truncated_id_to_full_id = {}
    for fid in feature_ranks_df.index:
        tfid = get_truncated_feature_id(fid)
        if tfid not in truncated_id_to_full_id:
            truncated_id_to_full_id[tfid] = fid
        else:
            logging.warning(
                "Indistinguishable rows in GNPS feature "
                "metadata file with truncated ID {}.".format(tfid)
            )
            # Replace the full feature ID with a bogus ID. This will prevent
            # the >= 2 full feature IDs from which the conflicting truncated
            # IDs were derived from getting annotated with anything -- better
            # to annotate less than to annotate incorrectly.
            truncated_id_to_full_id[tfid] = "rankratioviz_matching_conflict"

    metadata_df["rankratioviz_full_feature_id"] = metadata_df[
        "rankratioviz_trunc_feature_id"
    ].apply(lambda tfid: truncated_id_to_full_id[tfid])

    # Remove all rows in the metadata df with bogus full feature IDs,
    # which will let us use verify_integrity=True when setting index below.
    # There's definitely a faster way to do this than using iterrows(), but
    # this at least works
    indices_to_remove = []
    for idx, row in metadata_df.iterrows():
        if (
            row["rankratioviz_full_feature_id"]
            == "rankratioviz_matching_conflict"
        ):
            indices_to_remove.append(idx)

    metadata_df.drop(index=indices_to_remove, inplace=True)

    # Set the full feature ID column as the actual index of the DataFrame. If
    # there are any duplicates (due to two features having the same
    # mass-to-charge ratio and discharge time), our use of verify_integrity
    # here will raise an error accordingly. (That almost certainly won't
    # happen, # since we already look for indistinguishable truncated feature
    # IDs above, but best to be safe until this function is more rigorously
    # tested.)
    metadata_df.set_index(
        "rankratioviz_full_feature_id", verify_integrity=True, inplace=True
    )

    # Remove all the feature metadata that we don't care about (now, at least).
    # metadata_df now only contains the full feature ID we constructed and the
    # Library ID, so now it's ready to be used to annotate feature IDs from teh
    # ranks DataFrame.
    metadata_df = metadata_df.filter(items=["LibraryID"])
    return metadata_df