function [y] = rbm_unpreprocess(x, map)
x = unwhiten(x, map.whitenW, map.whitenb);
% initialize with as value the lower bound a; this will remain only for
% the dimensions that were removed in the preprocessing step
y = repmat(map.a, size(x, 1), 1);
y(:, ~map.ds) = x;
end
