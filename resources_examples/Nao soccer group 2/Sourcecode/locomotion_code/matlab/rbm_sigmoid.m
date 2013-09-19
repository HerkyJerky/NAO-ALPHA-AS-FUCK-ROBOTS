function [y] = rbm_sigmoid(x)
    y = 1 ./ (1 + exp(-x));
end
