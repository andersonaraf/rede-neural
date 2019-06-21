from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry, Region

ENDPOINT = "https://southcentralus.api.cognitive.microsoft.com"

# Replace with a valid key
training_key = "95b0a4720b9041f697a0b52d2e35cc33"
prediction_key = "cf621366042345548877b090e66aeff2"
prediction_resource_id = "/subscriptions/5d4d15d0-c922-41b5-81c3-f466c9a634bc/resourceGroups/IAProjects/providers/Microsoft.CognitiveServices/accounts/IAProjects_prediction"

publish_iteration_name = "detectModel"

trainer = CustomVisionTrainingClient(training_key, endpoint=ENDPOINT)

# Find the object detection domain
obj_detection_domain = next(domain for domain in trainer.get_domains() if domain.type == "ObjectDetection" and domain.name == "General")

# Create a new project
print ("Creating project...")
project = trainer.create_project("IA-Apple-Orange", domain_id=obj_detection_domain.id)

# Make two tags in the new project
fork_tag = trainer.create_tag(project.id, "maça")
scissors_tag = trainer.create_tag(project.id, "laranja")

fork_image_regions = {
    "maca_1": [  0.55, 0.46, 0.472, 0.505],
#    "maca_2": [ 0.294117659, 0.216944471, 0.534313738, 0.5980392 ],
#    "maca_3": [ 0.09191177, 0.0682516545, 0.757352948, 0.6143791 ],
#    "maca_4": [ 0.254901975, 0.185898721, 0.5232843, 0.594771266 ],
#    "maca_5": [ 0.2365196, 0.128709182, 0.5845588, 0.71405226 ],
#    "maca_6": [ 0.115196079, 0.133611143, 0.676470637, 0.6993464 ],
#    "maca_7": [ 0.164215669, 0.31008172, 0.767156839, 0.410130739 ],
#    "maca_8": [ 0.118872553, 0.318251669, 0.817401946, 0.225490168 ],
#    "maca_9": [ 0.18259804, 0.2136765, 0.6335784, 0.643790841 ],
#    "maca_10": [ 0.05269608, 0.282303959, 0.8088235, 0.452614367 ],
#    "maca_11": [ 0.05759804, 0.0894935, 0.9007353, 0.3251634 ],
#    "maca_12": [ 0.3345588, 0.07315363, 0.375, 0.9150327 ],
#    "maca_13": [ 0.269607842, 0.194068655, 0.4093137, 0.6732026 ],
#    "maca_14": [ 0.143382356, 0.218578458, 0.7977941, 0.295751631 ],
#    "maca_15": [ 0.19240196, 0.0633497, 0.5710784, 0.8398692 ],
#    "maca_16": [ 0.140931368, 0.480016381, 0.6838235, 0.240196079 ],
#    "maca_17": [ 0.305147052, 0.2512582, 0.4791667, 0.5408496 ],
#    "maca_18": [ 0.234068632, 0.445702642, 0.6127451, 0.344771236 ],
#    "maca_19": [ 0.219362751, 0.141781077, 0.5919118, 0.6683006 ],
#    "maca_20": [ 0.180147052, 0.239820287, 0.6887255, 0.235294119 ]
}

scissors_image_regions = {
#    "laranja_1": [ 0.4007353, 0.194068655, 0.259803921, 0.6617647 ],
#    "laranja_2": [ 0.426470578, 0.185898721, 0.172794119, 0.5539216 ],
#    "laranja_3": [ 0.289215684, 0.259428144, 0.403186262, 0.421568632 ],
#    "laranja_4": [ 0.343137264, 0.105833367, 0.332107842, 0.8055556 ],
#    "laranja_5": [ 0.3125, 0.09766343, 0.435049027, 0.71405226 ],
#    "laranja_6": [ 0.379901975, 0.24308826, 0.32107842, 0.5718954 ],
#    "laranja_7": [ 0.341911763, 0.20714055, 0.3137255, 0.6356209 ],
#    "laranja_8": [ 0.231617644, 0.08459154, 0.504901946, 0.8480392 ],
#    "laranja_9": [ 0.170343131, 0.332957536, 0.767156839, 0.403594762 ],
#    "laranja_10": [ 0.204656869, 0.120539248, 0.5245098, 0.743464053 ],
#    "laranja_11": [ 0.05514706, 0.159754932, 0.799019635, 0.730392158 ],
#    "laranja_12": [ 0.265931368, 0.169558853, 0.5061275, 0.606209159 ],
#    "laranja_13": [ 0.241421565, 0.184264734, 0.448529422, 0.6830065 ],
#    "laranja_14": [ 0.05759804, 0.05027781, 0.75, 0.882352948 ],
#    "laranja_15": [ 0.191176474, 0.169558853, 0.6936275, 0.6748366 ],
#    "laranja_16": [ 0.1004902, 0.279036, 0.6911765, 0.477124184 ],
#    "laranja_17": [ 0.2720588, 0.131977156, 0.4987745, 0.6911765 ],
#    "laranja_18": [ 0.180147052, 0.112369314, 0.6262255, 0.6666667 ],
#    "laranja_19": [ 0.333333343, 0.0274019931, 0.443627447, 0.852941155 ],
#    "laranja_20": [ 0.158088237, 0.04047389, 0.6691176, 0.843137264 ]
}
# Update this with the path to where you downloaded the images.
#base_image_url = "cognitive-services-python-sdk-samples/samples/vision/images"
base_image_url = "image"
# Go through the data table above and create the images
print ("Adicionando Imagens...")
tagged_images_with_regions = []

for file_name in fork_image_regions.keys():
    x,y,w,h = fork_image_regions[file_name]
    regions = [ Region(tag_id=fork_tag.id, left=x,top=y,width=w,height=h) ]

    with open(base_image_url + "/maca/" + file_name + ".png", mode="rb") as image_contents:
        tagged_images_with_regions.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), regions=regions))

for file_name in scissors_image_regions.keys():
    x,y,w,h = scissors_image_regions[file_name]
    regions = [ Region(tag_id=scissors_tag.id, left=x,top=y,width=w,height=h) ]

    with open(base_image_url + "/laranja/" + file_name + ".jpg", mode="rb") as image_contents:
        tagged_images_with_regions.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), regions=regions))

upload_result = trainer.create_images_from_files(project.id, images=tagged_images_with_regions)
if not upload_result.is_batch_successful:
    print("Falha na tentativa de envia imagem!")
    for image in upload_result.images:
        print("Status da Imagem: ", image.status)
    exit(-1)


#import time
#print ("Treinando...")
#iteration = trainer.train_project(project.id)
#while (iteration.status != "Completo"):
#    iteration = trainer.get_iteration(project.id, iteration.id)
#    print ("Status de treinamento: " + iteration.status)
#    time.sleep(1)

# The iteration is now trained. Publish it to the project endpoint
#trainer.publish_iteration(project.id, iteration.id, publish_iteration_name, prediction_resource_id)
#print ("Fim!")

    

