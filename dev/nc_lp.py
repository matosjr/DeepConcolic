
import cplex
import sys
import numpy as np

from utils import *

epsilon=1.0/(255)

def base_constraints(dnn):

  var_names=[]
  var_names_vect=[]
  objective=[] ## do we need 'objective' as base?
  lower_bounds=[]
  upper_bounds=[]

  the_index=0

  for l in range(0, len(dnn.layers)):
    ## we skip the last layer
    if l==len(dnn.layers)-1: continue

    layer=dnn.layers[l]

    print ('== {0} == \n'.format(l), layer)

    if is_input_layer(layer):
      osp=layer.input.shape ## the output at this layer
      if len(osp)<=2: 
        print ('== well, we do not think the input layer shall be non-convolutional... == \n')
        sys.exit(0)
      var_names.append(np.empty((1, osp[1], osp[2], osp[3]), dtype="S40"))
      for I in range(0, 1):
        for J in range(0, osp[1]):
          for K in range(0, osp[2]):
            for L in range(0, osp[3]):
              var_name='x_{0}_{1}_{2}_{3}_{4}'.format(the_index, I, J, K, L)
              objective.append(0)
              lower_bounds.append(-cplex.infinity)
              upper_bounds.append(cplex.infinity)
              var_names[the_index][I][J][K][L]=var_name
              var_names_vect.append(var_name)
    elif is_conv_layer(layer):
      if l==0: ## to deal with the input variables
        isp=layer.input.shape
        var_names.append(np.empty((1, isp[1], isp[2], isp[3]), dtype="S40"))
        for I in range(0, 1):
          for J in range(0, isp[1]):
            for K in range(0, isp[2]):
              for L in range(0, isp[3]):
                var_name='x_{0}_{1}_{2}_{3}_{4}'.format(the_index, I, J, K, L)
                objective.append(0)
                lower_bounds.append(-cplex.infinity)
                upper_bounds.append(cplex.infinity)
                var_names[the_index][I][J][K][L]=var_name
                var_names_vect.append(var_name)
      ##
      the_index+=1
      osp=layer.input.shape ## the output at this layer
      var_names.append(np.empty((1, osp[1], osp[2], osp[3]), dtype="S40"))
      for I in range(0, 1):
        for J in range(0, osp[1]):
          for K in range(0, osp[2]):
            for L in range(0, osp[3]):
              var_name='x_{0}_{1}_{2}_{3}_{4}'.format(the_index, I, J, K, L)
              objective.append(0)
              lower_bounds.append(-cplex.infinity)
              upper_bounds.append(cplex.infinity)
              var_names[the_index][I][J][K][L]=var_name
              var_names_vect.append(var_name)
      if act_in_the_layer(layer)=='relu':
        ##
        the_index+=1
        osp=layer.input.shape ## the output at this layer
        var_names.append(np.empty((1, osp[1], osp[2], osp[3]), dtype="S40"))
        for I in range(0, 1):
          for J in range(0, osp[1]):
            for K in range(0, osp[2]):
              for L in range(0, osp[3]):
                var_name='x_{0}_{1}_{2}_{3}_{4}'.format(the_index, I, J, K, L)
                objective.append(0)
                lower_bounds.append(-cplex.infinity)
                upper_bounds.append(cplex.infinity)
                var_names[the_index][I][J][K][L]=var_name
                var_names_vect.append(var_name)
    elif is_dense_layer(layer):
      if l==0: ## well, let us not allow to define a net starting with dense a layer...
        print ('well, let us not allow to define a net starting with dense a layer... ==\n')
        sys.exit(0)
      the_index+=1
      osp=layer.output.shape
      var_names.append(np.empty((1, osp[1]), dtype="S40"))
      for I in range(0, 1):
        for J in range(0, osp[1]):
          var_name='x_{0}_{1}_{2}'.format(the_index, I, J)
          objective.append(0)
          lower_bounds.append(-cplex.infinity)
          upper_bounds.append(cplex.infinity)
          var_names[the_index][I][J]=var_name
          var_names_vect.append(var_name)
      if act_in_the_layer(layer)=='relu':
        ##
        the_index+=1
        osp=layer.output.shape
        var_names.append(np.empty((1, osp[1]), dtype="S40"))
        for I in range(0, 1):
          for J in range(0, osp[1]):
            var_name='x_{0}_{1}_{2}'.format(the_index, I, J)
            objective.append(0)
            lower_bounds.append(-cplex.infinity)
            upper_bounds.append(cplex.infinity)
            var_names[the_index][I][J]=var_name
            var_names_vect.append(var_name)
    elif is_activation_layer(layer):
      if str(layer).find('relu')<0: continue ## well, we only consider ReLU activation layer
      the_index+=1
      osp=layer.output.shape
      if len(osp) > 2: ## multiple feature maps
        var_names.append(np.empty((1, osp[1], osp[2], osp[3]), dtype="S40"))
        for I in range(0, 1):
          for J in range(0, osp[1]):
            for K in range(0, osp[2]):
              for L in range(0, osp[3]):
                var_name='x_{0}_{1}_{2}_{3}_{4}'.format(the_index, I, J, K, L)
                objective.append(0)
                lower_bounds.append(-cplex.infinity)
                upper_bounds.append(cplex.infinity)
                var_names[the_index][I][J][K][L]=var_name
                var_names_vect.append(var_name)
      else:
        var_names.append(np.empty((1, osp[1]), dtype="S40"))
        for I in range(0, 1):
          for J in range(0, osp[1]):
            var_name='x_{0}_{1}_{2}'.format(the_index, I, J)
            objective.append(0)
            lower_bounds.append(-cplex.infinity)
            upper_bounds.append(cplex.infinity)
            var_names[the_index][I][J]=var_name
            var_names_vect.append(var_name)
    elif is_maxpooling_layer(layer):
      the_index+=1
      osp=layer.output.shape
      var_names.append(np.empty((1, osp[1], osp[2], osp[3]), dtype="S40"))
      for I in range(0, 1):
        for J in range(0, osp[1]):
          for K in range(0, osp[2]):
            for L in range(0, osp[3]):
              var_name='x_{0}_{1}_{2}_{3}_{4}'.format(the_index, I, J, K, L)
              objective.append(0)
              lower_bounds.append(-cplex.infinity)
              upper_bounds.append(cplex.infinity)
              var_names[the_index][I][J][K][L]=var_name
              var_names_vect.append(var_name)
    elif is_flatten_layer(layer):
      the_index+=1
      isp=layer.input.shape
      tot=int(isp[1]) * int(isp[2]) * int(isp[3])
      var_names.append(np.empty((1, tot), dtype="S40"))
      for I in range(0, 1):
        for J in range(0, tot):
          var_name='x_{0}_{1}_{2}'.format(the_index, I, J)
          objective.append(0)
          lower_bounds.append(-cplex.infinity)
          upper_bounds.append(cplex.infinity)
          var_names[the_index][I][J]=var_name
          var_names_vect.append(var_name)
    else:
      print ('Unknown layer', layer)
      sys.exit(0)

  constraints=[]
  rhs=[]
  constraint_senses=[]
  constraint_names=[]
  for I in range(0, var_names[0].shape[0]):
    for J in range(0, var_names[0].shape[1]):
      for K in range(0, var_names[0].shape[2]):
        for L in range(0, var_names[0].shape[3]):
          pass  ## we do not need it in the base...

  ## now, it comes the encoding of constraints
  weight_index=-1
  the_index=0
  tot_weights=dnn.get_weights()
  for l in range(0, len(dnn.layers)):
    ## we skip the last layer
    if l==len(dnn.layers)-1: continue

    layer=dnn.layers[l]

    print ('== {0} == \n'.format(l), layer)

    if is_input_layer(layer):
      continue
    elif is_conv_layer(layer):
      if l==0:
        the_index+=1
        continue
      the_index+=1
      isp=var_names[the_index-1].shape
      osp=var_names[the_index].shape
      kernel_size=layer.kernel_size
      weight_index+=1
      weights=tot_weights[weight_index]
      weight_index+=1
      biases=tot_weights[weight_index]
      for I in range(0, osp[0]):
        for J in range(0, osp[1]):
          for K in range(0, osp[2]):
            for L in range(0, osp[3]):
              print ('== ', l, ' == ', I, J, K, L)
              constraint=[[], []]
              constraint[0].append(var_names[the_index][I][J][K][L])
              constraint[1].append(-1)
              try:
                for II in range(0, kernel_size[0]):
                  for JJ in range(0, kernel_size[1]):
                    for KK in range(0, weights.shape[2]):
                      constraint[0].append(var_names[the_index-1][0][J+II][K+JJ][KK])
                      constraint[1].append(float(weights[II][JJ][KK][L]))
                constraints.append(constraint)
                rhs.append(-float(biases[L]))
                constraint_senses.append('E')
                constraint_names.append('')
              except: ## this is due to padding
                rhs.append(0)
                constraint_senses.append('E')
                constraint_names.append('')


def negate(dnn, act_inst, nc_layer, nc_pos):
  return None, None, None
