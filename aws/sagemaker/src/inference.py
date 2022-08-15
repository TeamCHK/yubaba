def model_fn(model_dir):
    model = T5ForConditionalGeneration.from_pretrained('t5-small')
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    with open(os.path.join(model_dir, 'model.pth'), 'rb') as f:
        model.load_state_dict(torch.load(f))
    model = model.to(device)
    return model


def input_fn(request_body, request_content_type):
#   encode
    return

def predict_fn(input_object, model):
#   generate
    return

def output_fn(prediction, response_content_type):
#   decode
    return