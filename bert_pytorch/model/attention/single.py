import torch.nn as nn
import torch.nn.functional as F
import torch

import math


class Attention(nn.Module):
    """
    Compute 'Scaled Dot Product Attention
    """

    def forward(self, query, key, value, mask=None, dropout=None):
        """
        Args: query, key, value 同源且 shape 相同
            query: [batch_size, head_num, seq_len, dim]
            key: [batch_size, head_num, seq_len, dim]
            value: [batch_size, head_num, seq_len, dim]
        """
        scores = torch.matmul(query, key.transpose(-2, -1)) \
                 / math.sqrt(query.size(-1))

        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)

        p_attn = F.softmax(scores, dim=-1)

        if dropout is not None:
            p_attn = dropout(p_attn)

        return torch.matmul(p_attn, value), p_attn
