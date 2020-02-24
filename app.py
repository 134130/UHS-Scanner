import cv2, os
import numpy as np

from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

@app.route('/')
def index():
    return render_template(
        'index.html',
        title   = 'Flask',
    )

@app.route('/upload', methods = ['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['pic']
        f.save('static/img/' + f.filename)
        return '<script>window.location.href = "/canvas?filename=' + f.filename + '";</script>'
        
        
@app.route('/canvas', methods = ['GET'])
def canvas():
    if request.method == 'GET':
        img_path = 'static/img/' + request.args.get('filename', '')
        ori_img = cv2.imread(img_path)

        return render_template(
            'canvas.html',
            width  = ori_img.shape[1],
            height = ori_img.shape[0],
            filepath = 'img/' + os.path.basename(img_path)
        )


@app.route('/pt', methods = ['GET'])
def pt():
    if request.method == 'GET':
        img_path = 'static/' + request.args.get('filename', '')
        filename, ext = os.path.splitext(os.path.basename(img_path))
        ori_img = cv2.imread(img_path)
        args = request.args
        src = [[int(args.get('x1')), int(args.get('y1'))],
               [int(args.get('x2')), int(args.get('y2'))],
               [int(args.get('x3')), int(args.get('y3'))],
               [int(args.get('x4')), int(args.get('y4'))]]

        src_np = np.array(src, dtype=np.float32)
        width = max(np.linalg.norm(src_np[0] - src_np[1]), np.linalg.norm(src_np[2] - src_np[3]))
        height = max(np.linalg.norm(src_np[0] - src_np[3]), np.linalg.norm(src_np[1] - src_np[2]))
        
        dst_np = np.array([
            [0, 0],
            [width, 0],
            [width, height],
            [0, height]
        ], dtype=np.float32)

        M = cv2.getPerspectiveTransform(src=src_np, dst=dst_np)
        result = cv2.warpPerspective(ori_img, M=M, dsize=(width, height))

        cv2.imwrite('static/result/%s_result%s' % (filename, ext), result)

        result_path = 'result/%s_result%s' % (filename, ext)
        return render_template(
            'result.html',
            filepath = result_path
        )


if __name__ == '__main__':
    app.run(debug = True)