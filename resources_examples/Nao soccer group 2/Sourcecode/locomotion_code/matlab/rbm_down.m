function [v] = rbm_down(rbm, h)
    v = rbm.sigmoid_down(bsxfun(@plus, h * rbm.W', rbm.bv));
end
