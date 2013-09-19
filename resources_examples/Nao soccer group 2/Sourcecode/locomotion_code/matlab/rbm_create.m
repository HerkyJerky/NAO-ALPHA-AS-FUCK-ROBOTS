function [rbm] = rbm_create(nv, nh)
rbm = [];

rbm.sample_up = @rbm_sample_binary;
rbm.sample_down = @identity;
rbm.sigmoid_up = @rbm_sigmoid;
rbm.sigmoid_down = @rbm_sigmoid;

% numbers of visible and hidden units
rbm.nv = nv; rbm.nh = nh;
% weights, visible bias, hidden bias
rbm.W = zeros(nv, nh); rbm.bv = zeros(1, nv); rbm.bh = zeros(1, nh);
end
