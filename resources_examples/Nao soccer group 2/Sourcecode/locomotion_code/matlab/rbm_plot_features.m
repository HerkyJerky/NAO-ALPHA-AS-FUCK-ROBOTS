function [handle, collage] = rbm_plot_features(rbm)
    v = eye(rbm.nh) * rbm.W';
    [handle, collage] = plot_patches(normalize(v));
end
