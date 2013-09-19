function [x] = normalize(x)
%NORMALIZE scale and translate into [0,1]
a = min(x(:));
b = max(x(:));
x = (x - a)/(b - a);
end

