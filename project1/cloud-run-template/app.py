from flask import Flask, render_template, request
from google.cloud import pubsub_v1


app = Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def test_page():
    project = "cpsc5387"
    if request.method == 'POST':
        action = request.form['action']
        pubsub_topic = "storage_server_build"
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project, pubsub_topic)
        future = publisher.publish(topic_path, data=b'Best message ever!', action=action)
        print(future.result())
    page_template = 'base_template.html'
    return render_template(page_template)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
