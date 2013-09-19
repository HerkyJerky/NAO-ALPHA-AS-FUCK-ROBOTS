function [rbm] = rbm_initialize_parameters(rbm, x, options)
    b = 4 * sqrt(6 / (rbm.nv + rbm.nh));
    a = -b;
    W = rand(rbm.nv, rbm.nh) * (b-a) + a;

    % estimate probability of each visible unit being on (wrt data x)
    pv = mean(x, 1);
    bv = log(max(1e-10, pv ./ max(1e-10, (1 - pv))));
    
    bh = options.desired_sparsity * ones(1, rbm.nh);
    % how about this instead?
    %bh = binornd(1, options.desired_sparsity, [1, rbm.nh]);
    
    % now turn some of this off to see what happens
    %W = zeros(rbm.nv, rbm.nh);
    %bv = zeros(1, rbm.nv);
    %bh = zeros(1, rbm.nh);

    rbm.W = W;
    rbm.bv = bv;
    rbm.bh = bh;
end
