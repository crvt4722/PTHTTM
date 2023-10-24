from flask import Flask, jsonify, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)


@app.route('/model/name', methods=['GET'])
def read():
    return "hello"



# @app.route('/api/update', methods=['POST'])
# def update_post():
#     try:
#         data = request.get_json()
#         update_data(
#             data['id'], data['name'], data['username'], data['birth'], data['sex'], data['university'], data['major']
#         )
#
#         return jsonify(data)
#     except:
#         return "Error!"


# @app.route('/api/delete/<int:id>')
# def delete_post(id):
#     id = str(id)
#     try:
#         if id != '29':
#             delete_data(id)
#         return redirect("http://localhost:8000/")
#     except:
#         return "Error!"



if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5000)
    app.run(host='0.0.0.0', port=9090, debug=True)