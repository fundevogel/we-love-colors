<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>PANTONE® color palettes</title>

    <style media="screen">
      <?php include('../examples.css') ?>
    </style>
  </head>
  <body>
    <?php
        // GLOBAL FUNCTIONS & VARIABLES
        $file = '../../palettes/pantone/colors.json';
    ?>
    <h1>PANTONE® color palettes</h1>

    <!-- COPYRIGHT NOTICE -->
    <header>
      PANTONE® and related trademarks are the property of <a href="https://www.pantone.com">Pantone LLC</a>,
      a division of <a href="https://www.xrite.com">X-Rite</a>, a <a href="https://www.danaher.com">Danaher</a> company.
    </header>

    <?php include('../grid.php') ?>

    <!-- CLIPBOARD.JS -->
    <script>
      <?php include('../clipboard.js') ?>
    </script>
  </body>
</html>
<body>
