<?php
if ($route === 'admin/logout') { session_destroy(); header('Location: /admin/login'); exit; }
if ($route === 'admin/login') {
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        verify_csrf(); $now=time(); $attempts=array_values(array_filter($_SESSION['login_attempts']??[],static fn($t)=>$t>$now-900));
        if(count($attempts)>=5){$_SESSION['login_attempts']=$attempts;http_response_code(429);$error='尝试次数过多，请 15 分钟后再试。';}
        else { $rows=query('SELECT * FROM admins WHERE username=?',[$_POST['username']??'']); if($rows&&password_verify($_POST['password']??'',$rows[0]['password_hash'])){unset($_SESSION['login_attempts']);session_regenerate_id(true);$_SESSION['admin_id']=$rows[0]['id'];header('Location: /admin');exit;} $attempts[]=$now;$_SESSION['login_attempts']=$attempts;$error='用户名或密码错误'; }
    }
    render('admin/login',['title'=>'管理员登录','error'=>$error??null]);exit;
}
require_admin();
if($_SERVER['REQUEST_METHOD']==='POST'){
 verify_csrf();
 if($route==='admin/settings'){
  if (isset($_POST['form_hiddify'])) {
    set_setting('show_hiddifysales', isset($_POST['show_hiddifysales']) ? '1' : '0');
  }
  if (isset($_POST['form_seo'])) {
    set_setting('google_verification', preg_replace('/[^a-zA-Z0-9_-]/', '', (string)($_POST['google_verification'] ?? '')) ?? '');
    set_setting('baidu_verification', preg_replace('/[^a-zA-Z0-9_-]/', '', (string)($_POST['baidu_verification'] ?? '')) ?? '');
    $gtm = strtoupper(trim((string)($_POST['gtm_id'] ?? '')));
    $gtm = preg_replace('/[^A-Z0-9-]/', '', $gtm) ?? '';
    if ($gtm !== '' && !preg_match('/^GTM-[A-Z0-9]+$/', $gtm)) {
      $gtm = '';
    }
    set_setting('gtm_id', $gtm);
  }
  header('Location: /admin?saved=1'); exit;
 }
 if($route==='admin/articles/delete'){db()->prepare('DELETE FROM articles WHERE id=?')->execute([(int)$_POST['id']]);}
 elseif($route==='admin/articles/bulk'){$ids=array_values(array_filter(array_map('intval',$_POST['ids']??[])));$action=$_POST['bulk_action']??'';if($ids&&in_array($action,['publish','draft','delete'],true)){$marks=implode(',',array_fill(0,count($ids),'?'));if($action==='delete')db()->prepare("DELETE FROM articles WHERE id IN ($marks)")->execute($ids);else db()->prepare("UPDATE articles SET status=?,published_at=IF(?='published',COALESCE(published_at,NOW()),NULL) WHERE id IN ($marks)")->execute(array_merge([$action,$action],$ids));}}
 elseif($route==='admin/articles/save'){
  $id=(int)($_POST['id']??0);$status=($_POST['status']??'draft')==='published'?'published':'draft';$published=$status==='published'?(($_POST['published_at']??'')?str_replace('T',' ',$_POST['published_at']).':00':date('Y-m-d H:i:s')):null;$content=sanitize_article_html((string)($_POST['content_html']??''));$faq=json_encode(array_values(array_filter($_POST['faq']??[],static fn($x)=>trim($x['q']??'')!==''&&trim($x['a']??'')!=='')),JSON_UNESCAPED_UNICODE);$sources=json_encode(array_values(array_filter($_POST['sources']??[],static fn($x)=>filter_var($x['url']??'',FILTER_VALIDATE_URL))),JSON_UNESCAPED_UNICODE);$featured=isset($_POST['featured'])?1:0;$popular=isset($_POST['popular'])?1:0;$image=trim((string)($_POST['image_url']??''));$alt=trim((string)($_POST['image_alt']??''));
  if(!empty($_FILES['image_file']['tmp_name']) && is_uploaded_file($_FILES['image_file']['tmp_name'])){
    $tmp=$_FILES['image_file']['tmp_name']; $size=(int)$_FILES['image_file']['size'];
    if($size>2*1024*1024){ http_response_code(400); exit('Image too large'); }
    $finfo=new finfo(FILEINFO_MIME_TYPE); $mime=$finfo->file($tmp);
    $map=['image/jpeg'=>'jpg','image/png'=>'png','image/webp'=>'webp','image/svg+xml'=>'svg'];
    if(!isset($map[$mime])){ http_response_code(400); exit('Unsupported image type'); }
    $name=bin2hex(random_bytes(8)).'.'.$map[$mime]; $dest=dirname(__DIR__).'/public/uploads/'.$name;
    if(!move_uploaded_file($tmp,$dest)){ http_response_code(500); exit('Upload failed'); }
    @chmod($dest,0644); $image='/uploads/'.$name;
  }
  if($id){db()->prepare('UPDATE articles SET title=?,slug=?,seo_title=?,meta_description=?,content_html=?,status=?,published_at=?,is_featured=?,is_popular=?,image_url=?,image_alt=?,faq_json=?,sources_json=? WHERE id=?')->execute([$_POST['title'],$_POST['slug'],$_POST['seo_title'],$_POST['meta_description'],$content,$status,$published,$featured,$popular,$image,$alt,$faq,$sources,$id]);}
  else{db()->prepare('INSERT INTO articles(title,slug,seo_title,meta_description,content_html,status,published_at,is_featured,is_popular,image_url,image_alt,faq_json,sources_json) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)')->execute([$_POST['title'],$_POST['slug'],$_POST['seo_title'],$_POST['meta_description'],$content,$status,$published,$featured,$popular,$image,$alt,$faq,$sources]);$id=(int)db()->lastInsertId();}
  $cats=array_values(array_filter(array_map('intval',$_POST['category_ids']??[])));db()->prepare('DELETE FROM article_category WHERE article_id=?')->execute([$id]);$link=db()->prepare('INSERT INTO article_category(article_id,category_id) VALUES(?,?)');foreach($cats as $cat)$link->execute([$id,$cat]);
 }
 elseif($route==='admin/articles/preview'){
  $_SESSION['preview_article']=['title'=>$_POST['title']??'','slug'=>$_POST['slug']??'preview','seo_title'=>$_POST['seo_title']??'','meta_description'=>$_POST['meta_description']??'','content_html'=>sanitize_article_html((string)($_POST['content_html']??'')),'categories'=>'预览','category_slugs'=>'','published_at'=>date('Y-m-d H:i:s'),'updated_at'=>date('Y-m-d H:i:s'),'image_url'=>$_POST['image_url']??'','image_alt'=>$_POST['image_alt']??'','faq_json'=>json_encode(array_values(array_filter($_POST['faq']??[],static fn($x)=>trim($x['q']??'')!=='')),JSON_UNESCAPED_UNICODE),'sources_json'=>json_encode(array_values(array_filter($_POST['sources']??[],static fn($x)=>filter_var($x['url']??'',FILTER_VALIDATE_URL))),JSON_UNESCAPED_UNICODE),'id'=>0];
  header('Location: /admin/preview'); exit;
 }
 header('Location: /admin/articles');exit;
}
if($route==='admin'){
  $stats=(int)db()->query("SELECT COUNT(*) FROM articles WHERE status='published'")->fetchColumn();
  $drafts=(int)db()->query("SELECT COUNT(*) FROM articles WHERE status='draft'")->fetchColumn();
  render('admin/dashboard',[
    'title'=>'管理后台',
    'stats'=>$stats,
    'drafts'=>$drafts,
    'showHiddify'=>show_hiddifysales(),
    'saved'=>isset($_GET['saved']),
    'googleVerification'=>setting('google_verification'),
    'baiduVerification'=>setting('baidu_verification'),
    'gtmId'=>setting('gtm_id'),
  ]);
  exit;
}
if($route==='admin/analytics'){
  $range=$_GET['range']??'30d';
  if(!in_array($range,['today','7d','30d','90d'],true)) $range='30d';
  render('admin/analytics',[
    'title'=>'访问统计',
    'robots'=>'noindex,nofollow',
    'report'=>analytics_dashboard($range),
  ]);
  exit;
}
if($route==='admin/articles'){$articles=query('SELECT * FROM articles ORDER BY created_at DESC');render('admin/articles',['title'=>'文章管理','articles'=>$articles]);exit;}
if($route==='admin/articles/new'){$cats=query('SELECT * FROM categories ORDER BY id');render('admin/editor',['title'=>'新建文章','article'=>['id'=>0,'title'=>'','slug'=>'','seo_title'=>'','meta_description'=>'','content_html'=>'','status'=>'draft','published_at'=>'','is_featured'=>0,'is_popular'=>0,'image_url'=>'','image_alt'=>'','faq_json'=>'[]','sources_json'=>'[]'],'categories'=>$cats,'selectedCategories'=>[]]);exit;}
if(preg_match('#^admin/articles/(\\d+)/edit$#',$route,$m)){$items=query('SELECT * FROM articles WHERE id=?',[(int)$m[1]]);if(!$items){http_response_code(404);render('pages/404',['title'=>'页面未找到']);exit;}$cats=query('SELECT * FROM categories ORDER BY id');$selected=array_column(query('SELECT category_id FROM article_category WHERE article_id=?',[(int)$m[1]]),'category_id');render('admin/editor',['title'=>'编辑文章','article'=>$items[0],'categories'=>$cats,'selectedCategories'=>$selected]);exit;}
if($route==='admin/preview'){ if(empty($_SESSION['preview_article'])){header('Location: /admin/articles');exit;} $article=$_SESSION['preview_article']; render('articles/show',['article'=>$article,'title'=>'预览：'.($article['seo_title']?:$article['title']),'description'=>$article['meta_description']]); exit; }
http_response_code(404);render('pages/404',['title'=>'页面未找到']);
