function [x, W, b] = whiten(x, W, b)
%WHITEN ZCA whitening that can deal with singular x
epsilon = 1e-5;
if nargin < 3
    b = mean(x, 1);
end
x = bsxfun(@minus, x, b);
if nargin < 2
    [U S] = svd(x');
    W = U * diag(1./sqrt(diag(S) + epsilon)) * U';
end
x = x * W;
end
