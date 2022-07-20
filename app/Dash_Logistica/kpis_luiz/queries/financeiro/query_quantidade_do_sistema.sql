SELECT (SELECT SUM(Quantidade * TipoOperacao) AS Expr1
                  FROM      Estoque.XMovimentacaoEstoque AS E
                  WHERE   (IdProduto = EM.IdProduto) AND (IdEstoque = EM.IdEstoque) AND (IdTipoMovimentacao <> 1)) AS Quantidade, IdProduto, CodigoProduto, IdEstoque
FROM     Estoque.XMovimentacaoEstoque AS EM WITH (NOLOCK)
WHERE  (IdEstoque in (1,5))
GROUP BY IdProduto, CodigoProduto, IdEstoque