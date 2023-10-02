import pandas as pd


# explode text's words to words column
def _explode_text_words(df, text_column):

    df["words"] = df[text_column].str.split()
    return df.explode("words")


def _get_nodes(df, node_id, node_label, node_type, node_metadata=None):
    if node_metadata is None:
        node_metadata = []
    nodes = {}

    data = df.to_dict("records")

    for l in data:
        nodes[l[node_id]] = {
            "label": l[node_label],
            "type": node_type,
            "metadata": {meta: l[meta] for meta in node_metadata},
        }

    return nodes


def process_nodes(drugs, pubmed, clinical_trials):
    # get drugs nodes
    nodes = _get_nodes(drugs, node_id="atccode", node_type="drug", node_label="drug")
    # get pubmed nodes
    nodes.update(
        _get_nodes(
            pubmed,
            node_id="id",
            node_type="pubmed",
            node_label="title",
            node_metadata=["journal"],
        )
    )
    # get clinical_trials nodes
    nodes.update(
        _get_nodes(
            clinical_trials,
            node_id="id",
            node_type="clinical_trial",
            node_label="scientific_title",
            node_metadata=["journal"],
        )
    )
    # get journals nodes
    nodes.update(
        _get_nodes(pubmed, node_id="journal", node_type="journal", node_label="journal")
    )
    nodes.update(
        _get_nodes(
            clinical_trials,
            node_id="journal",
            node_type="journal",
            node_label="journal",
        )
    )


def process_edges(drugs, pubmed, clinical_trials):
    # explode words
    pubmed = _explode_text_words(pubmed, "title")
    clinical_trials = _explode_text_words(clinical_trials, "scientific_title")

    # link publications to drugs
    pubmed_drugs = pd.merge(pubmed, drugs, left_on="words", right_on="drug")[
        ["id", "atccode", "date", "journal"]
    ].drop_duplicates()
    clinical_trials_drugs = pd.merge(
        clinical_trials, drugs, left_on="words", right_on="drug"
    )[["id", "atccode", "date", "journal"]].drop_duplicates()

    # link journal to drugs
    journal_drugs = pd.concat(
        [
            clinical_trials_drugs[["journal", "atccode", "date"]],
            pubmed_drugs[["journal", "atccode", "date"]],
        ],
        ignore_index=True,
    ).drop_duplicates()

    # pubmed, drugs edges
    edges = _get_edges(
        pubmed_drugs,
        src_node="atccode",
        dst_node="id",
        edge_label="referenced_in",
        edge_metadata=["date"],
    )

    # clinical_trials, drugs edges
    edges.append(
        _get_edges(
            clinical_trials_drugs,
            src_node="atccode",
            dst_node="id",
            edge_label="referenced_in",
            edge_metadata=["date"],
        )
    )
    # journal, drugs edges
    edges.append(
        _get_edges(
            journal_drugs,
            src_node="atccode",
            dst_node="journal",
            edge_label="referenced_in",
            edge_metadata=["date"],
        )
    )


def _get_edges(df, src_node, dst_node, edge_label, edge_metadata=None):

    if edge_metadata is None:
        edge_metadata = []

    edges = []
    data = df.to_dict("records")

    for l in data:
        edges.append(
            {
                "src": l[src_node],
                "dst": l[dst_node],
                "label": edge_label,
                "metadata": {meta: l[meta] for meta in edge_metadata},
            }
        )

    return edges
