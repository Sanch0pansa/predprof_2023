<template>
  <section class="hero">
    <div class="row">
      <div class="col-lg-7">
        <h1>Мониторинг интернет-ресурсов российских ВУЗов</h1>
        <p class="fs-5 my-4 text-muted">Сервис по автоматической проверке доступности интернет-ресурсов российскийх высших учебных заведений, сбору информации о работе сайтов, учету сообщений пользователей о сбоях.</p>
        <Btn>Добавить ресурс</Btn>
      </div>
      <div class="col-lg-5">
        <div class="advs">
          <div class="adv">
            <i class="fas fa-robot text-primary fs-1"></i>
            <span>Автоматический мониторинг</span>
          </div>
          <div class="adv">
            <i class="fas fa-paper-plane text-primary fs-1"></i>
            <span>Оповещения в телеграм</span>
          </div>
          <div class="adv">
            <i class="fas fa-comment text-primary fs-1"></i>
            <span>Сбор сообщений пользователей</span>
          </div>
          <div class="adv">
            <i class="fas fa-star text-primary fs-1"></i>
            <span>Рейтинг<br>ресурсов</span>
          </div>
        </div>
      </div>
    </div>
  </section>

</template>

<script>
export default {
  name: "PageWelcomeSection",
}
</script>

<style scoped>

</style>