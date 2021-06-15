<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
    </head>
    <body>
        <div class="ui container" style="padding-top: 10px;">
        <h1>Recommendations</h1>
        <a href="/news">Back to the News</a>
        <table class="ui celled table">
            <thead>
                <th>Title</th>
                <th>Author</th>
                <th>#Likes</th>
                <th>#Comments</th>
                <th colspan="3">Label</th>
            </thead>
            <tbody>
                <tr>
                    <td class="positive" colspan="7">Вам будет интересно:</td>
                </tr>
                %for row in positive:
                <tr>
                    <td><a href="{{ row[0].url }}" alt="row[1]">{{ row[0].title }}</a></td>
                    <td>{{ row[0].author }}</td>
                    <td>{{ row[0].points }}</td>
                    <td>{{ row[0].comments }}</td>
                    <td class="positive"><a href="/add_label/?label=good&id={{ row[0].id }}&back=classify">Интересно</a></td>
                    <td class="active"><a href="/add_label/?label=maybe&id={{ row[0].id }}&back=classify">Возможно</a></td>
                    <td class="negative"><a href="/add_label/?label=never&id={{ row[0].id }}&back=classify">Не интересно</a></td>
                </tr>
                %end
                <tr>
                    <td class="active" colspan="7">Возможно, вам стоит прочитать:</td>
                </tr>
                %for row in active:
                <tr>
                    <td><a href="{{ row[0].url }}" alt="row[1]">{{ row[0].title }}</a></td>
                    <td>{{ row[0].author }}</td>
                    <td>{{ row[0].points }}</td>
                    <td>{{ row[0].comments }}</td>
                    <td class="positive"><a href="/add_label/?label=good&id={{ row[0].id }}&back=classify">Интересно</a></td>
                    <td class="active"><a href="/add_label/?label=maybe&id={{ row[0].id }}&back=classify">Возможно</a></td>
                    <td class="negative"><a href="/add_label/?label=never&id={{ row[0].id }}&back=classify}">Не интересно</a></td>
                </tr>
                %end
                <tr>
                    <td class="negative" colspan="7">Вам будет неинтересно:</td>
                </tr>
                %for row in negative:
                <tr>
                    <td><a href="{{ row[0].url }}" alt="row[1]">{{ row[0].title }}</a></td>
                    <td>{{ row[0].author }}</td>
                    <td>{{ row[0].points }}</td>
                    <td>{{ row[0].comments }}</td>
                    <td class="positive"><a href="/add_label/?label=good&id={{ row[0].id }}&back=classify">Интересно</a></td>
                    <td class="active"><a href="/add_label/?label=maybe&id={{ row[0].id }}&back=classify">Возможно</a></td>
                    <td class="negative"><a href="/add_label/?label=never&id={{ row[0].id }}&back=classify">Не интересно</a></td>
                </tr>
                %end
            </tbody>
            <tfoot class="full-width">
                <tr>
                    <th colspan="7">
                        <a href="/update/?back=classify" class="ui right floated small primary button">I Wanna more Hacker News!</a>
                    </th>
                </tr>
            </tfoot>
        </table>
        </div>
    </body>
</html>
