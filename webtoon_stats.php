<html>
<head>
    <meta charset="UTF-8">
    <meta name = "viewport" content="width = device-width, height=device-height, initial-scale=1.0">
    <title>Daily Webtoon Stats</title>
    <link rel="stylesheet" href="webtoon_carousel.css">
    <link rel="stylesheet" href="webtoon_comment.css">
</head>

<body>
    <div class = "carousel">
        
        <button class="arrow up" id ="prev"></button>
        <button class="arrow down" id = "next"></button> 

        <ul>
            <li class="slide active">
                    <!-- TODO: Get the webtoon name with php -->
                    <!-- <img src="images/Naver_Line_Webtoon_logo.png" alt="the webtoon logo" class="smol"/> -->
                    <div class = "title">Webtoon statistics of: </div>
            

            <?php

            


            # connect to database and show
            include('webtoon_credentials.php');
            ini_set('display_errors', 1);
            error_reporting(E_ALL);
            $connect = mysqli_connect('localhost', DB_USER, DB_PASSWORD, 'webtoon_scraping');
            
            $query =   'SELECT name FROM webtoons LIMIT 1;';
            $result = mysqli_query($connect, $query);
            $row = mysqli_fetch_assoc($result);

            echo $row['name'];
            echo '</li>';
            

            # all database requests
            # request 1
            echo '<li class="slide">';
            $query =   'SELECT COUNT(content) as nb_comments, username
                        FROM top_comments, users
                        WHERE users.id = top_comments.id_user
                        GROUP BY id_user
                        ORDER BY nb_comments DESC
                        LIMIT 3;';

            $result = mysqli_query($connect, $query);
            echo  "les 3 personnes qui ont été le plus de fois dans les top commentaires <br>";
            while($row = mysqli_fetch_assoc($result)){
                echo $row['nb_comments'] . " " . $row['username'] . "<br>";
            }
            echo '</li>';

            # request 2
            echo '<li class="slide">';
            $query =   'SELECT username, content, nb_upvotes, nb_downvotes
                        FROM top_comments, users
                        WHERE users.id = top_comments.id_user
                        ORDER BY nb_upvotes DESC
                        LIMIT 1;'; 

            $result = mysqli_query($connect, $query);
            $row = mysqli_fetch_assoc($result);


            # comment block
            echo '<p> Le commentaire qui a le plus de like: </p>';
            echo '<div class="comment_container">
                    <div class="username">' .$row['username']. '</div>
                    <div class="comment_content">'  . $row['content'] . '</div>
                    <div class="votes">
                        <div class="upvote_block">
                            <img src="../images/upvote_c.svg" />
                            <div class="upvote_count">'  . $row['nb_upvotes'] . '</div>
                        </div>
                        <div class="downvote_block">
                            <img src="../images/downvote_c.svg" />
                            <div class="downvote_count"> '  . $row['nb_downvotes'] .'</div>
                        </div>
                    </div>
                </div>';   
            echo '</li>';

            # request 3
            echo '<li class="slide">';
            $query =   'SELECT username, content, nb_upvotes, nb_downvotes
                        FROM top_comments, users
                        WHERE users.id = top_comments.id_user
                        ORDER BY nb_downvotes DESC
                        LIMIT 1;'; 

            $result = mysqli_query($connect, $query);
            $row = mysqli_fetch_assoc($result);

            # comment block
            echo '<p> Le commentaire qui a le plus de dislike: </p>';
            echo '<div class="comment_container">
                    <div class="username">' .$row['username']. '</div>
                    <div class="comment_content">'  . $row['content'] . '</div>
                    <div class="votes">
                        <div class="upvote_block">
                            <img src="../images/upvote_c.svg" />
                            <div class="upvote_count">'  . $row['nb_upvotes'] . '</div>
                        </div>
                        <div class="downvote_block">
                            <img src="../images/downvote_c.svg" />
                            <div class="downvote_count"> '  . $row['nb_downvotes'] .'</div>
                        </div>
                    </div>
                </div>'; 
            echo '</li>';

            # request 4
            echo '<li class="slide">';
            $query  =  'SELECT username, content, LENGTH(content) as len_content, nb_upvotes, nb_downvotes
                        FROM top_comments, users
                        WHERE users.id = top_comments.id_user
                        ORDER BY len_content DESC
                        LIMIT 1;';
            
            $result = mysqli_query($connect, $query);
            $row = mysqli_fetch_assoc($result);

            # comment block
            echo '<p> Le commentaire le plus long: </p>';
            echo '<div class="comment_container">
                    <div class="username">' .$row['username']. '</div>
                    <div class="comment_content">'  . $row['content'] . '</div>
                    <div class="votes">
                        <div class="upvote_block">
                            <img src="../images/upvote_c.svg" />
                            <div class="upvote_count">'  . $row['nb_upvotes'] . '</div>
                        </div>
                        <div class="downvote_block">
                            <img src="../images/downvote_c.svg" />
                            <div class="downvote_count"> '  . $row['nb_downvotes'] .'</div>
                        </div>
                    </div>
                </div>'; 
            echo '</li>';

            # request 5
            echo '<li class="slide">';
            $query  =  'SELECT username, content, LENGTH(content) as len_content, nb_upvotes, nb_downvotes
                        FROM top_comments, users
                        WHERE users.id = top_comments.id_user
                        ORDER BY len_content ASC
                        LIMIT 1;';
            
            $result = mysqli_query($connect, $query);
            $row = mysqli_fetch_assoc($result);

            # comment block
            echo '<p> Le commentaire le plus court: </p>';
            echo '<div class="comment_container">
                    <div class="username">' .$row['username']. '</div>
                    <div class="comment_content">'  . $row['content'] . '</div>
                    <div class="votes">
                        <div class="upvote_block">
                            <img src="../images/upvote_c.svg" />
                            <div class="upvote_count">'  . $row['nb_upvotes'] . '</div>
                        </div>
                        <div class="downvote_block">
                            <img src="../images/downvote_c.svg" />
                            <div class="downvote_count"> '  . $row['nb_downvotes'] .'</div>
                        </div>
                    </div>
                </div>'; 

            echo '</li>';
            
            echo '<li class="slide"><li>';

            mysqli_close($connect);
            
            ?>
        </ul>
    </div>
    <script src="webtoon_carousel.js"></script>
</body>
</html>
