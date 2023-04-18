function my_scope() {
    const forms = document.querySelectorAll('.form-delete');
  
    for (const form of forms) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
  
        const confirmed = confirm('Tem certeza de que deseja excluir essa receita?');
  
        if (confirmed) {
          form.submit();
        }
      });
    }
  }
  
  my_scope();