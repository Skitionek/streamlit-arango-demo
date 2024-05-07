"""app.py"""
import streamlit as st
from arango import ArangoClient, AQLQueryKillError

from streamlit_arango_demo.config import Config

# Initialize the ArangoDB client.
client = ArangoClient(hosts=Config.ArangoDB.host)

st.title("ArangoDB Demo")

col1, col2 = st.columns([0.7, 0.3])

with col1:
    query = st.text_area(
        key="query",
        value="RETURN LENGTH(test_collection)",
        label="Query editor",
        placeholder="Enter a query",
        help="Type a arango query to execute",
    )

    """Query preview"""
    query_preview = st.code(
        body=st.session_state.query,
        language="aql"
    )

with col2:
    """Query variables"""
    bind_vars = st.data_editor(
        key="bind_vars",
        data={
            "key": "value"
        },
        num_rows='dynamic',
        use_container_width=True,
        column_config={
            "_index": st.column_config.TextColumn("Key"),
            "value": st.column_config.TextColumn("Value")
        }
    )


def connect_to_db():
    # Initialize connection to database.
    if 'db' not in st.session_state:
        # Connect to "test" database as root user.
        st.session_state.db = client.db(
            name=Config.ArangoDB.database,
            username=Config.ArangoDB.username,
            password=Config.ArangoDB.password
        )
        st.write(f"Connected to database '{st.session_state.db.name}' as {st.session_state.db.username}.")

    return st.session_state.db


def get_aql():
    return connect_to_db().aql


if st.button("Execute", use_container_width=True):
    # Get the AQL API wrapper.
    aql = get_aql()

    with st.status("Executing query...", expanded=False) as status:
        # Retrieve the execution plan without running the query.
        st.write("Retrieving execution plan...")
        plan = aql.explain(query)

        """Execution plan"""
        st.json(plan, expanded=False)

        # Validate the query without executing it.
        st.write("Validate query...")
        validation = aql.validate(query)

        """Validation result"""
        st.json(validation, expanded=False)

        st.write("Execute query...")
        cursor = aql.execute(
            query,
            bind_vars=bind_vars
        )
        status.update(label="Query executed successfully. Click for details", state="complete")

    """Results"""
    st.table(cursor)

with st.sidebar:
    """Utilities"""
    # List currently running queries.
    with st.popover("Running queries", use_container_width=True):
        # Get the AQL API wrapper.
        aql = get_aql()
        queries = aql.queries()
        st.table(queries)

    # List any slow queries.
    with st.popover("Slow queries", use_container_width=True):
        # Get the AQL API wrapper.
        aql = get_aql()
        slow_queries = aql.slow_queries()
        st.table(slow_queries)

    # Clear slow AQL queries if any.
    if st.button("Clear slow queries", use_container_width=True):
        # Get the AQL API wrapper.
        aql = get_aql()
        aql.clear_slow_queries()

    # Retrieve AQL query tracking properties.
    with st.popover("Tracking properties", use_container_width=True):
        # Get the AQL API wrapper.
        aql = get_aql()
        tracking = aql.tracking()
        st.json(tracking)

    with st.popover("Set tracking properties", use_container_width=True):
        # Configure AQL query tracking properties.
        """Tracking properties"""
        tracking_properties = st.data_editor(
            key="tracking_properties",
            data={
                "key": "value"
            },
            use_container_width=True,
            num_rows='dynamic',
            column_config={"key": {"editable": True}, "value": {"editable": True}}
        )
        if st.button("Set", use_container_width=True):
            # Get the AQL API wrapper.
            aql = get_aql()
            aql.set_tracking(*tracking_properties)

    with st.popover("Kill query", use_container_width=True):
        # Kill a running query (this should fail due to invalid ID).
        kill_id = st.number_input("Query id to kill", help="Enter the query id to kill", )
        if st.button("Kill", use_container_width=True):
            # Get the AQL API wrapper.
            aql = get_aql()
            try:
                aql.kill(kill_id)
            except AQLQueryKillError as err:
                assert err.http_code == 404
                assert err.error_code == 1591
