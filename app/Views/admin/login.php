<div class="container page-stack">
  <section class="prose">
    <h1>管理员登录</h1>
    <?php if (!empty($error)): ?><p><?=e($error)?></p><?php endif; ?>
    <form method="post">
      <input type="hidden" name="csrf" value="<?=e(csrf())?>">
      <label class="form-field">用户名<input name="username" required autocomplete="username"></label>
      <label class="form-field">密码<input type="password" name="password" required autocomplete="current-password"></label>
      <button class="button button-dark" type="submit">登录</button>
    </form>
  </section>
</div>
