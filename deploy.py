import mxnet as mx

from rcnn.utils.load_model import load_param
from rcnn.symbol import gensym

DATA_NAMES = ['data', 'im_info']
LABEL_NAMES = None
DATA_SHAPES = [('data', (1, 3, 600, 1000)), ('im_info', (1, 3))]
LABEL_SHAPES = None

def deploy_net(prefix, epoch, ctx = mx.cpu()):
    sym = gensym.gen_sym_infer()
    arg_params, aux_params = load_param(prefix, epoch, convert=True, ctx=ctx, process=True)
    mod = mx.module.Module(sym, DATA_NAMES, None, ctx)
    mod.bind(DATA_SHAPES, LABEL_SHAPES, for_training=False)

    mod.set_params(arg_params=arg_params, aux_params=aux_params)

    mod.save_checkpoint(prefix + '_deploy', 0)

if __name__ == '__main__':
    deploy_net('./model/rpn1', 12)