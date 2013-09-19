function [x] = unwhiten(x, W, b)
x = bsxfun(@plus, x / W, b);
end
