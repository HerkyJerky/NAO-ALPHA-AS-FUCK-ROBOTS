function [x, map] = rbm_preprocess(x, map)
%RBM_PREPROCESS 
%   remove constant dimensions, whiten
if nargin < 2
    map = [];
    map.a = min(x, [], 1);
    map.b = max(x, [], 1);
    % remove constant dimensions
    map.ds = map.a == map.b;
end
x(:, map.ds) = [];
if nargin < 2
    [x map.whitenW map.whitenb] = whiten(x);
else
    x = whiten(x, map.whitenW, map.whitenb);
end
end
