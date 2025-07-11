import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    return (pd,)


@app.cell
def _(mo):
    mo.md(r"""# Functions""")
    return


@app.cell
def _(pd):
    def generate_mermaid_er_diagram(df: pd.DataFrame) -> str:
        """
        Generates Mermaid ER diagram code from a Pandas DataFrame of database constraints.

        Args:
            df: A Pandas DataFrame with the following columns:
                - 'table_name' (str): The name of the table containing the foreign key.
                - 'column_name' (str): The name of the column that is the foreign key.
                - 'foreign_table_name' (str): The name of the referenced table.
                - 'foreign_column_name' (str): The name of the referenced column in the foreign table.

        Returns:
            str: The complete Mermaid ER diagram code.
        """
        # Start the Mermaid ER diagram block
        mermaid_code_lines = ["erDiagram"]

        # Use a set to keep track of unique table definitions to avoid duplicates
        # Mermaid automatically defines tables when relationships are drawn,
        # but explicitly defining them can sometimes be useful for clarity or
        # to include column definitions if desired (though not requested here).
        # For this specific request, we'll let Mermaid implicitly define them.

        # Iterate through each row of the DataFrame to generate relationship lines
        for index, row in df.iterrows():
            table_name = row['table_name']
            column_name = row['column_name']
            foreign_table_name = row['foreign_table_name']
            foreign_column_name = row['foreign_column_name']

            # Construct the Mermaid relationship line based on the specified template
            # table_name --column_name--> foreign_table_name --> foreign_column_name
            relationship_line = (
                f"    {table_name} -- {column_name} --> {foreign_table_name} : {foreign_column_name}"
            )
            mermaid_code_lines.append(relationship_line)

        # Join all lines to form the complete Mermaid code
        return "\n".join(mermaid_code_lines)
    return


@app.cell
def _(mo):
    mo.md(r"""# Workflow""")
    return


@app.cell
def _(pd):
    table_with_constraints = pd.read_csv("~/constraints.csv")
    return (table_with_constraints,)


@app.cell
def _(mo):
    mo.md(r"""# Scratch""")
    return


@app.cell
def _(table_with_constraints):
    table_with_constraints[table_with_constraints['table_name'] == 'atgcat']
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
