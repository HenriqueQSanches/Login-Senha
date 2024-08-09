/* -------------------------------------------------------------------------------------------------- */
                        /* ANOTAÇÕES IMPORTANTES DE DESENVOLVIMENTO */
/* Adicionar o código <script src="{% static 'js/script.js' %}?v={% now 'U' %}"></script> para que o 
o Python atualize a versão nova do Script a cada carregamento de página. */

/* Adicionei essa observação devido a ter ficado horas tentando entender porque o script não
atualizava no meu projeto, e quando descobri, resolvi anotar para futuros desenvolvimentos */

/* -------------------------------------------------------------------------------------------------- */
function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
  }
  
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
  }
/* -------------------------------------------------------------------------------------------------- */


/* -------------------------------------------------------------------------------------------------- */
                        /* FUNÇÃO DE CONFIRMAÇÃO PARA EXCLUIR CADASTRO */

function confirmDelete(event) {
  event.preventDefault();  // Evita o envio automático do formulário

  if (confirm("Isso irá excluir todo seu cadastro do site, você tem certeza?")) {
      document.getElementById('deleteForm').submit();  // Envia o formulário se o usuário confirmar
  }
}
/* -------------------------------------------------------------------------------------------------- */