<template>
<header class="py-4 bg-white shadow">
  <div class="container">
    <nav class="navbar">
      <a class="navbar-brand" href="#">SiteChecker</a>
<!--      <ul class="navbar-nav flex flex-row gap-3">-->
<!--        <li class="nav-item">-->
<!--          <a class="nav-link active" aria-current="page" href="#">Home</a>-->
<!--        </li>-->
<!--        <li class="nav-item">-->
<!--          <a class="nav-link" href="#">Features</a>-->
<!--        </li>-->
<!--        <li class="nav-item">-->
<!--          <a class="nav-link" href="#">Pricing</a>-->
<!--        </li>-->
<!--        <li class="nav-item">-->
<!--          <a class="nav-link disabled">Disabled</a>-->
<!--        </li>-->
<!--      </ul>-->
      <ul class="navbar-nav">
        <li v-if="$store.state.isAuth" class="nav-item dropstart">
          <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            user@site.com
            <i class="ms-2 fa-solid fa-user text-primary"></i>
          </a>
          <ul class="dropdown-menu" style="position: absolute;">
            <li><a class="dropdown-item" href="#">Личный кабинет</a></li>
          </ul>
        </li>
        <li v-else class="nav-item">
          <a href="">Log in</a>
        </li>
      </ul>
    </nav>
  </div>
</header>
</template>

<script>
export default {
  name: "PageHeader"
}
</script>

<style scoped>

</style>