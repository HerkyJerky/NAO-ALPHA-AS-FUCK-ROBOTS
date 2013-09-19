function [x] = rbm_sample(p)
% sample binary states from probabilities
    x = binornd(1, p, size(p));
end
