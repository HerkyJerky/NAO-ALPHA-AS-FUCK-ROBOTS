function [rbm] = rbm_widen(rbm, k, x, options)
%RBM_WIDEN add k hidden units with random initialization, but don't touch
% the weights for the pre-existent hidden units
% x and options are used to initialize as in rbm_initialize_parameters
rbm2 = rbm_create(rbm.nv, k);
rbm2 = rbm_initialize_parameters(rbm2, x, options);

rbm.W = [rbm.W rbm2.W];
rbm.bh = [rbm.bh rbm2.bh];
rbm.nh = rbm.nh + rbm2.nh;
end
