"""
Van Nguyen
Tradeshift Mid level coding exercise.
6/15/2020
filename: api.py
"""

from abstract_database_connection import AbstractDatabaseConnection
from flask import Flask, jsonify, request
import node

amazingco = Flask(__name__)

@amazingco.route('/nodes/<string:node>', methods=['GET'])
def get(node):
    """ 
    Get all descendant nodes of a given node.

    Args:
        node: node identifier.
    Returns:
        Response message with HTTP code.
    """
    node_name = {'node': node}
    result = get_descendant(node)
    if (result):
        http_response = 200
        message = 'Descendant node(s) of {}: {} '.format(node, result)
    elif (len(result) == 0):
        http_response = 200
        message = 'Node {} does not have any descendant node.'.format(node)
    else:
        http_response = 400
        message = 'Could not get descendant nodes of {} .'.format(node)
    return build_result(message, http_response)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
@amazingco.route('/nodes/<string:node>', methods=['PUT'])
def update(node):
    """
    Change the parent node of a given node.

    Args:
        node: node identifier.
    Returns:
        Response message with HTTP code.
    """
    new_parent = request.args.get('new_parent')
    result = change_parent(node, new_parent)
    if (result):
        http_response = 200
        message = 'Updated node {} to new parent node {}'.format(node, new_parent)
    else:
        http_response = 400
        message = 'Could not update node {}'.format(node)
    return build_result(message, http_response)

def build_result(content, http_status):
    """
    Build API response.

    Args:
        content: message content.
        http_status: HTTP status code.
    Returns:
        API response with message and HTTP code.
    """
    success = True if (http_status == 200) else False
    if (success):
        return jsonify({
            "success": 'true',
            "response": content,
            "code": http_status
        })
    else:
        return jsonify({
            "success": 'false',
            "error": {
                "code": http_status,
                "message": "Error: {}".format(content)
            }
        })

def get_descendant(parent_node):
    """
    Get a row from the specified table with given row id.

    Args:
        table_name: a valid table in the database.
        row_id: a valid row of said table.
    Returns:
        A row from the database.
    """
    with AbstractDatabaseConnection('amazingco.db') as conn:
        column = "parent_name"
        sql_statement = "SELECT name FROM node WHERE {} = '{}' AND is_current = 1;".format(column, parent_node)
        cursor = conn.cursor()
        rows_count = cursor.execute(sql_statement)
        if (rows_count):
            result = ', '.join([r[0] for r in cursor.fetchall()])
            return result
        else:
            return None

def change_parent(node, new_parent):
    with AbstractDatabaseConnection('amazingco.db') as conn:
        # archiving the old parent-descendant pair
        sql_statement = "UPDATE node SET is_current = 0 WHERE name = '{}' AND is_current = 1;".format(node)
        cursor = conn.cursor()
        cursor.execute(sql_statement)
        # gather info about new parent node (root node, height)
        new_parent_statement = "SELECT root_name, height FROM node WHERE name = '{}'".format(new_parent)
        cursor = conn.cursor()
        qresult = cursor.execute(new_parent_statement)
        if (qresult):
            for r in cursor.fetchall():
                root_node = r[0]
                new_height = int(r[1]) + 1
                # insert new parent-descentdant node pair
                insert_statement = "INSERT INTO node(name, parent_name, root_name, height) VALUES ('{}', '{}', '{}', {})".format(node, new_parent, root_node, new_height)
                cursor = conn.cursor()
                cursor.execute(insert_statement)
                conn.commit()
                return True
        else:
            return False

if __name__ == '__main__':
    # TODO: Turn off debugging in production.
    amazingco.run(debug=True)
