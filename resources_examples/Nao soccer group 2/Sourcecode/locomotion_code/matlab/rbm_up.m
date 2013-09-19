function [h] = rbm_up(rbm, v)
    h = rbm.sigmoid_up(bsxfun(@plus, v * rbm.W, rbm.bh));
end
