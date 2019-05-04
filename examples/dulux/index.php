<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Dulux® color palettes</title>

    <style media="screen">
      <?php include('../examples.css') ?>
    </style>
  </head>
  <body>
    <?php
        // GLOBAL FUNCTIONS & VARIABLES
        $files = glob('../../palettes/dulux/json/*/*.json');
    ?>
    <h1>Dulux® color palettes</h1>

    <!-- COPYRIGHT NOTICE -->
    <header>
      Dulux® and related trademarks are the property of <a href="https://www.akzonobel.com">AkzoNobel N.V.</a>
      (dutch joint-stock company) (worldwide) and <a href="https://www.dulux.com.au">DuluxGroup</a> (Australia & New Zealand).
    </header>

    <?php include('../grid.php') ?>

    <!-- CLIPBOARD.JS -->
    <script>
      <?php include('../clipboard.js') ?>
    </script>
  </body>
</html>
<body>
