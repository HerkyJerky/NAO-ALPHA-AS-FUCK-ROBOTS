function [dW, dbv, dbh, q] = rbm_updates(rbm, x, q, options)
[dfe_W, dfe_bv, dfe_bh, qnew] = rbm_cdn(rbm, options.chain_length, x);
q = options.sparsity_estimate_decay * q + (1 - options.sparsity_estimate_decay) * qnew;
sparsity_penalty = options.sparsity_cost * (q - options.desired_sparsity);
%weight_penalty = options.weight_cost * rbm.W; % L2 weight penalty
weight_penalty = options.weight_cost * sign(rbm.W); % L1 weight penalty
dW = options.learning_rate * bsxfun(@minus, dfe_W - weight_penalty, sparsity_penalty);
dbv = options.learning_rate * dfe_bv;
dbh = options.learning_rate * (dfe_bh - sparsity_penalty);
end
