from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

app = ClarifaiApp(api_key='bccfacc1fd5048a59e8ac070459fa45d')
m = app.models.get('general-v1.3')

def get_predictions(imgs):
    result = []
    imgs_list = []
    for image_path in imgs:
        image = ClImage(file_obj=open(image_path, 'rb'))
        imgs_list.append(image)
#        result.append(m.predict([image]))
    return m.predict(imgs_list)

