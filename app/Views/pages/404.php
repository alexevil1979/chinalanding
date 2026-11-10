<div class="container page-stack">
  <section class="empty">
    <h1><?=e(t('page_not_found'))?></h1>
    <p><?=e(locale()==='zh'?'你访问的地址不存在或已被移动。':(locale()==='ru'?'Запрошенный адрес не существует или был перемещён.':'The address you requested does not exist or has moved.'))?></p>
    <a class="button button-dark" href="<?=e(lp('/'))?>"><?=e(t('home'))?></a>
  </section>
</div>
