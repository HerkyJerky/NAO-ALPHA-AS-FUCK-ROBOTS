function [] = imshow(x, range)
    if nargin < 2
        range = [min(x(:)) max(x(:))];
    end
    x = (x - range(1)) / (range(2) - range(1));
    image(x * 255);
    colormap(gray(256));
end
