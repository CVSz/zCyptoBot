import torch


def maml_step(model, loss_fn, x: torch.Tensor, y: torch.Tensor, lr: float = 1e-2):
    y_pred = model(x)
    loss = loss_fn(y_pred, y)
    grads = torch.autograd.grad(loss, model.parameters(), create_graph=True)

    fast_weights = [param - lr * grad for param, grad in zip(model.parameters(), grads)]
    return fast_weights, loss
