<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>HKS® color palettes</title>

    <style media="screen">
      <?php include('../examples.css') ?>
    </style>
  </head>
  <body>
    <?php
        // GLOBAL FUNCTIONS & VARIABLES
        $file = '../../palettes/hks/colors.json';
    ?>
    <h1>HKS® color palettes</h1>

    <!-- COPYRIGHT NOTICE -->
    <header>
      HKS® and related trademarks are the property of <a href="https://www.hks-farben.de">HKS Warenzeichenverband e.V</a>
    </header>

    <?php include('../grid.php') ?>

    <!-- CLIPBOARD.JS -->
    <script>
      <?php include('../clipboard.js') ?>
    </script>
  </body>
</html>
<body>
