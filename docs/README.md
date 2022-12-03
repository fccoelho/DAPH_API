<style>
    body {
    counter-reset: h2
    }

    h2 {
        counter-reset: h3
    }

    h3 {
        counter-reset: h4
    }

    h4 {
        counter-reset: h5
    }

    h2:before {
        counter-increment: h2;
        content: counter(h2) ". "
    }

    h3:before {
        counter-increment: h3;
        content: counter(h2) "." counter(h3) ". "
    }

    h4:before {
        counter-increment: h4;
        content: counter(h2) "." counter(h3) "." counter(h4) ". "
    }

    h5:before {
        counter-increment: h5;
        content: counter(h2) "." counter(h3) "." counter(h4) "." counter(h5) ". "
    }
</style>

# Documentações do projeto 
# Avaliações das revisões

## Introdução

Neste projeto, anseia-se desenvolver um método para a avaliação das revisões feitas nos artigos submetidos na plataforma DAPH (_Decentralized Autonomous Publishing House_), considerando que isso é de suma importância para a validação dos artigos e do funcionamento da proposta de solução para a comunicação científica de maneira descentralizada. 

Essas avaliações são, resumidamente, "notas" que os usuários da plataforma vão poder atribuir às revisões feitas em cada artigo, de forma que seja feita uma classificação (e desclassificação) das revisões assim como dos revisores com base numa média ponderada dessas notas.

Nesse contexto, isso deve ser implementado na parte de _software_ no _back-end_ (a lógica que rege como as avaliações interagem com o sistema) e no _front-end_ (a apresentação interativa para o usuário final) da plataforma para que a funcionalidade seja incorporada no resultado final para os usuários possam utilizar.


## Especificações
  
Têm-se em vista que a avaliação das revisões deve ser de tal forma que não somente crie um _ranking_ das avaliações em ordem de importância (ou qualidade de avaliação, a depender da interpretação) mas também possa "desclassificar" revisões tendenciosas (conluios, rivalidades e outras formas de viés que prejudiquem o método científico). Isto é, é importante se atentar que uma revisão mal avaliada possa, em certos casos, levá-la a não ser considerada para o aprimoramento e a aprovação do artigo, assim como também isso impacta na classificação de participação e importância dos próprios revisores (dado que a classificação desses membros é parte fundamental para a que eles alcancem o _status_ de revisor - _reviewers_).
  
Dessa forma, é razoável que avaliação da revisão seja feita não apenas de forma binária, como "aprovado" e "não aprovado", ou "_upvote_" e "_downvote_", mas que possa ser atribuída uma "nota" numa escala (discreta, mas  que possa ser convertida em contínua) como um número inteiro (ou com uma casa decimal, possivelmente aceitando apenas 0 ou 5 - representando "meio ponto" na nota) no intervalo fechado de 0 (zero) a 10 (dez), de forma que seria possível calcular uma média ponderada das avaliações, com os pesos sendo as classificação de participação de cada usuário que avaliou.

Além disso, por fim, é razoável que uma avaliação no contexto científico venha acompanhada de justificativas e não apenas seja realizada de forma completamente arbitrária e não auditável. Nesse sentido, as avaliações devem vir acompanhadas de comentários (textuais) que descrevem o motivo da nota que foi atribuída, para que seja possível que outros usuários reportem uma avaliação tendenciosa (como descrito para o caso de revisões tendenciosas) e ela seja desconsiderada.  

## Avaliações das revisões
No contexto de avaliações das revisões, devemos levar em conta diversos fatores, como serão melhor descritos a seguir.

O cálculo para as avaliações das revisões e reputações dos usuários foi desenvolvido a partir das características do projeto. Nesse sentido, foi pesquisado como funciona a [reputação do stack overflow](https://stackoverflow.com/help/whats-reputation), porém acreditamos que o método utilizado nesse caso deve ser diferente, principalmente pela pouca valorização a qualidade das interações dos usuários (no geral, a reputação do stack overflow valoriza mais a quantidade de interações positivas, e não muito a qualidade de cada interação), o que acreditamos que não seja o melhor quando se trata de avaliarmos os manuscritos, as revisões e os usuários com uma metodologia científica.

### Reputação dos usuários
Sugerimos que os cálculos a respeito das pontuações (reputação, _score_) de cada usuário sejam feitos a partir:
+ Das pontuações dos manuscritos submetidos, e
+ Das pontuações das revisões.

Nesse sentido, a reputação de cada usuário deve ser calculada como uma média ponderada das pontuações da seguinte forma:

$$
R = 
\frac
{
    \sum\limits_{i = 1}^{N_M} 
        P_{M_i} \cdot N_{R_i}
} 
{
    \sum\limits_{i = 1}^{N_M} N_{R_i}
} 
$$

Onde temos:
+ $R$: reputação do usuário;
+ $P_{M_i}$: pontuação dos manuscritos;
+ $N_{R_i}$: número de revisões dos manuscritos, e
+ $N_M$: número de manuscritos.


<!-- Com isso, cada usuário deverá ter pontuações distintas, cada uma com respeito a cada um dos itens acima. Isso deve ser feito para distinguirmos futuramente os pesos nas distribuições -->

### Pontuação dos manuscritos
A pontuação dos manuscritos deve ser calculada como uma média aritmética, da forma: 
$$
P_{M_i} =
\frac
{
    \sum\limits_{i = 1}^{N_R} P_{R_i} 
}{
    N_{R}
}
$$

Onde temos:
+ $P_{R_i}$: pontuação das revisões que estabeleceram os critérios mínimos e (ou) foram consideradas realmente.
+ $N_R$: número de revisões que satisfaçam como acima

### Pontuação das revisões
Por sua vez, o cálculo das pontuações das revisões deve uma média ponderada com os pesos sendo as reputações dos usuários que avaliaram. De forma que:
$$
P_{R_i} =
\frac
{
    \sum\limits_{i = 1}^{N_A} P_{A_i} \cdot N_{A_i}  
}{
    \sum\limits_{i = 1}^{N_A} N_{A_i} 
}
$$

Onde temos:
+ $P_{A_i}$: pontuação da avaliação
+ $N_{A_i}$: número de avaliações


### Aprovação de revisões
Para cada manuscrito submetido, devemos ter 2 revisores, isto é, duas revisões aprovadas que o autor vai receber como válidas, dessa maneira, devemos ter um critério de aprovação (ou reprovação) de revisões.

Caso não existam revisões suficientes que satisfaçam os critérios mínimos, pegamos o restante pela ordem de pontuação das revisões.
#### Número mínimo de avaliações
Devemos, em primeiro lugar, considerar que caso um manuscrito receba muitas revisões e cada revisão receba muitas avaliações, devemos priorizar as revisões que possuam um número razoável de avaliações, pois podemos entender que ela passou pela aprovação de mais pessoas para ser considerada boa. Assim, devemos levar em consideração um número mínimo (absoluto ou percentual) de avaliações para uma revisão ser aprovada.

Nesse sentido, é proposto que cada revisão deve ter no mínimo:
$$
N_{A_{min}} = 
\begin{cases}
3 \text{, se $N_I < 30$} \\
\frac{N_I}{10} \text{, se $N_I \geq 30$}
\end{cases}
$$

Onde temos:
+ $N_I$: número de interações que foram feitas com um manuscrito (total de revisões, avaliações e _reports_).

#### Pontuação mínima
No mesmo sentido do número mínimo de avaliações que uma revisão deve receber, também devemos estabelecer uma pontuação mínima da revisão para ela ser aprovada.

Sugere-se um mínimo padrão de 70\% do pontuação máxima possível de uma avaliação, porém esse valor é completamente subjetivo, então podemos deixar a escolha também ao autor que submeter um manuscrito para revisão para que ele escolha qual deve ser a pontuação mínima de uma revisão para ela ser aprovada.

### Desconsideração de avaliações
Deve ser desconsideradas as avaliações enviesadas (mal intencionadas - evitar conluios, conflitos de interesses, etc), pois, apesar de esperarmos que idealmente esses casos não venham a existir, temos que ter em mente que é muito complicado garantir que uma avaliação seja imparcial e também que não existam usuários mal intencionados.

A ideia para sinalizar que avaliações devem ser desconsideradas é criar um campo de _report_ para que os usuários marquem uma _flag_ negativa para a avaliação, que deve também receber obrigatoriamente um motivo da anotação da _flag_ negativa (devem ser definidos valores padrão) e opcionalmente uma explicação mais completa do motivo.

#### Número mínimo de _reports_ 
Devemos definir um número mínimo de _reports_ para redirecionar a avaliação para o comitê decidir se ela deve ser excluída ou não. Nesse sentido, sugerimos que esse número seja calculado de forma identica ao número mínimo de avaliações de uma revisão definido anteriormente.

#### Penalidades pela avaliação excluída
Tendo em vista que as avaliações enviesadas são nocivas para o ecossistema do projeto como um todo, sugerimos que sejam definidas penalidade (padrão) para o usuário que tiver a avaliação excluída por _reports_, como:

+ Redução da reputação do usuários após cada avaliação excluída (com duração de 6 meses)
+ Suspensão da conta por um mês após 3 avaliações excluídas, e
+ Suspensão por tempo indeterminado da conta após reincidência de suspensão (ou seja, após 6 avaliações excluídas).

### Incentivos
Para que o ecossistema do projeto funcione, devem existir incentivos para cada etapa de interação dos usuários, para que os usuários tenham interesse em contribuir com as revisões dos manuscritos e o projeto como um todo.
#### Avaliação da revisão
Para realizar uma avaliação de revisão, sugerimos que os usuários recebam um incentivo na forma de tokens (como pagamento), uma fração dos tokens que são pagos pelos autores para submeter os manuscritos para revisão, porém uma porcentagem menor que as revisões.

#### Reportar avaliação da revisão
Com relação a reportar uma avaliação de revisão, sugerimos que o incentivo na realidade seja uma medida restritiva, de forma que quando um usuário interage com um manuscrito fazendo uma revisão ou uma avaliação, ele tenha que realizar uma quantidade mínima de avaliações da necessidade de _reports_ nas avaliações relacionadas ao mesmo manuscrito (sendo possível anotar que uma revisão não precisa de _report_). 

Nesse sentido, sugerimos que os usuários precisem avaliar a necessidade de _report_ de 20\% da quantidade total de avaliações de revisões relacionadas com o manuscrito, sem exceder um máximo de 10 avaliações. Também podem ser difinidos critérios para penalizar usuários que não reportem avaliações que foram excluídas por motivos como, por exemplo, "avaliação sem justificativa" (ou com o campo de justificativa preenchido com algo não relacionado a revisão).

Entretanto, deve ser possível deixar qualquer usuários realizar _reports_ caso desejado, sem ser de forma obrigatória, e sem fazer com que isso implique no usuário ter que avaliar a necessidade de _report_ em outras avaliações relacionadas ao mesmo manuscrito.


