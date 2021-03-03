from modin_spreadsheet import (
    SpreadsheetWidget,
    set_defaults,
    show_grid,
    on as widget_on,
)
from traitlets import All
import numpy as np

# import pandas as pd
import modin.pandas as pd
import json


def create_df():
    return pd.DataFrame(
        {
            "A": 1.0,
            "Date": pd.Timestamp("20130102"),
            "C": pd.Series(1, index=list(range(4)), dtype="float32"),
            "D": np.array([3] * 4, dtype="int32"),
            "E": pd.Categorical(["test", "train", "foo", "bar"]),
            "F": ["foo", "bar", "buzz", "fox"],
        }
    )


def test_apply_history():
    df = create_df()
    another_df = df.copy()

    spreadsheet = SpreadsheetWidget(df=df)

    spreadsheet._handle_view_msg_helper(
        {
            "row_index": 1,
            "column": "A",
            "unfiltered_index": 1,
            "value": 5,
            "type": "edit_cell",
        }
    )
    spreadsheet._handle_view_msg_helper(
        {
            "type": "change_filter",
            "field": "A",
            "filter_info": {"field": "A", "type": "slider", "min": None, "max": 4.14},
        },
    )

    spreadsheet._handle_view_msg_helper(
        {
            "row_index": 2,
            "column": "F",
            "unfiltered_index": 3,
            "value": "foo",
            "type": "edit_cell",
        }
    )

    spreadsheet._handle_view_msg_helper(
        {
            "type": "change_filter",
            "field": "Date",
            "filter_info": {
                "field": "Date",
                "type": "date",
                "min": 1356998400000,
                "max": 1357171199999,
            },
        }
    )
    spreadsheet._handle_view_msg_helper(
        {"type": "change_sort", "sort_field": "Date", "sort_ascending": True}
    )
    spreadsheet._handle_view_msg_helper(
        {
            "row_index": 1,
            "column": "A",
            "unfiltered_index": 2,
            "value": 2,
            "type": "edit_cell",
        }
    )
    spreadsheet._handle_view_msg_helper(
        {
            "row_index": 2,
            "column": "A",
            "unfiltered_index": 3,
            "value": 3,
            "type": "edit_cell",
        }
    )

    spreadsheet.apply_history(another_df)

    assert another_df.equals(df)


if __name__ == "__main__":
    test_apply_history()


"""
"# Edit cell\ndf.loc[(1, 'A')]=5; # Filter columns\ndf = unfiltered_df[(unfiltered_df['A'] <= 4.14)].copy(); # Edit cell\ndf.loc[(3, 'F')]='foo'; # Filter columns\ndf = unfiltered_df[(unfiltered_df['A'] <= 4.14)&(unfiltered_df['Date'] >= pd.to_datetime(1356998400000, unit='ms'))&(unfiltered_df['Date'] <= pd.to_datetime(1357171199999, unit='ms'))].copy(); # Sort column\ndf.sort_values('Date', ascending=True, inplace=True); # Edit cell\ndf.loc[(2, 'A')]=2; # Edit cell\ndf.loc[(3, 'A')]=3"
"""