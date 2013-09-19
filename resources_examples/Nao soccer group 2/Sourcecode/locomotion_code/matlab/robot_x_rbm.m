dataset = load('linewalk');

[dataset.x, xmap] = rbm_preprocess(dataset.x);

xtrain = dataset.x(1:24999, :);
xvalid = dataset.x(25000:end, :);

xperm = randperm(size(xtrain, 1));
xtrain = xtrain(xperm, :);

options = [];
options.learning_rate = 0.00001;
options.batch_size = 30;
options.chain_length = 1;
options.sparsity_cost = 0.5;
options.desired_sparsity = 0.1;
options.sparsity_estimate_decay = 0.9;
options.weight_cost = 0.00001;
options.initial_momentum = 0.5;
options.final_momentum = 0.9;
options.overfitting_estimate_decay = 0.9;
options.overfitting_threshold = 1; % no idea here
options.validation_interval = 5;

rbm = rbm_create(size(xtrain, 2), 256);
rbm.sample_up = @identity;
rbm.sample_down = @identity;
rbm.sigmoid_up = @rbm_sigmoid;
rbm.sigmoid_down = @identity;
rbm = rbm_initialize_parameters(rbm, xtrain, options);

[rbm, continuation] = rbm_train(rbm, xtrain, xvalid, 100, options);
