<?php
    // See https://stackoverflow.com/a/34244525
    function slugify(string $string)
    {
        return strtolower(trim(preg_replace('/[^A-Za-z0-9-]+/', '-', $string)));
    }
?>

<!-- CREATING TABLE OF CONTENTS -->
<?php
    echo '<ul>';
    foreach ($files as $file) :
    $start = ['_', '-colors'];
    $end = [' (', ' Colors)'];
    $title = str_replace($start, $end, ucwords(basename($file, '.json')));
?>
    <li>
      <a href="#<?= slugify($title) ?>"><?= $title ?></a>
    </li>
<?php
    endforeach;
    echo '</ul>';
?>


<!-- CREATING GRID -->
<?php
    foreach ($files as $file) :

    // GRID TITLE
    $start = ['_', '-colors'];
    $end = [' (', ' Colors)'];
    $title = str_replace($start, $end, ucwords(basename($file, '.json')));
?>
<h2 id="<?= slugify($title) ?>">
  <?= $title ?> - <a href="#">Back to top &uarr;</a>
</h2>

<?php
    // GRID CONTENT
    echo '<div class="grid">';

    $json = file_get_contents($file);
    $set = json_decode($json, true);

    foreach ($set as $color) :
    $name = $color['name'] !== '' ? $color['name'] : $color['code'];
?>
    <div class="grid_item" style="background-color: <?= $color['hex'] ?>" data-clipboard-text="<?= $color['hex'] ?>">
      <h3><?= $name ?></h3>
    </div>
<?php endforeach ?>

<?php
    echo '</div>';
    endforeach;
?>
