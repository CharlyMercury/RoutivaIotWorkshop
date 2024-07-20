export async function getIots() {
  const items = [
    {
      slug: "comedor",
      title: "Comedor",
      description: "Aquí puedes comer",
      image:
        "https://content.elmueble.com/medio/2024/01/12/asi-se-disena-un-comedor-para-que-sea-facil-de-limpiar_00000000_a792b683_240112130103_600x600.jpg",
    },
    {
      slug: "sala",
      title: "Sala",
      description: "Aquí puedes ver tv",
      image:
        "https://mueblesvizcaya.com.mx/wp-content/uploads/2023/10/SALA-INDONDESIA.png",
    },
    {
      slug: "dormitorio",
      title: "Dormitorio",
      description: "Aquí puedes dormir",
      image:
        "https://dormitorios.blog/wp-content/uploads/2022/12/Dormitorios-modernos.jpg",
    },
    {
      slug: "descanso",
      title: "Descanso",
      description: "Aquí puedes descansar",
      image:
        "https://as2.ftcdn.net/v2/jpg/01/67/73/97/1000_F_167739713_vYJIgXVO50AKeKp5pdXbOynSYKVUMH87.jpg",
    },
    {
      slug: "azotea",
      title: "Azotea",
      description: "Aquí puedes hacer fiestas",
      image:
        "https://i0.wp.com/www.glosarioarquitectonico.com/wp-content/uploads/2015/12/azotea3.jpg?ssl=1",
    },
    {
      slug: "jardin",
      title: "Jardin",
      description: "Aquí puedes plantar",
      image:
        "https://puntimmobiliari.com/wp-content/uploads/2021/03/casa-jardin.jpg",
    },
    {
      slug: "exterior",
      title: "Exterior",
      description: "Aquí es la calle",
      image:
        "https://inelba.com/wp-content/uploads/2021/08/iluminar-exterior-de-casa.jpg",
    },
  ];

  return items.map((item) => {
    const { description, slug, title, image } = item;

    return {
      description,
      slug,
      title,
      image,
    };
  });
}

export async function getIotsDetails(slug) {
  const items = {
    comedor: {
      slug: "comedor",
      title: "Comedor",
      description: "Aquí puedes comer",
      image:
        "https://content.elmueble.com/medio/2024/01/12/asi-se-disena-un-comedor-para-que-sea-facil-de-limpiar_00000000_a792b683_240112130103_600x600.jpg",
    },
    sala: {
      slug: "sala",
      title: "Sala",
      description: "Aquí puedes ver tv",
      image:
        "https://mueblesvizcaya.com.mx/wp-content/uploads/2023/10/SALA-INDONDESIA.png",
    },
    dormitorio: {
      slug: "dormitorio",
      title: "Dormitorio",
      description: "Aquí puedes dormir",
      image:
        "https://dormitorios.blog/wp-content/uploads/2022/12/Dormitorios-modernos.jpg",
    },
    descanso: {
      slug: "descanso",
      title: "Descanso",
      description: "Aquí puedes descansar",
      image:
        "https://as2.ftcdn.net/v2/jpg/01/67/73/97/1000_F_167739713_vYJIgXVO50AKeKp5pdXbOynSYKVUMH87.jpg",
    },
    azotea: {
      slug: "azotea",
      title: "Azotea",
      description: "Aquí puedes hacer fiestas",
      image:
        "https://i0.wp.com/www.glosarioarquitectonico.com/wp-content/uploads/2015/12/azotea3.jpg?ssl=1",
    },
    jardin: {
      slug: "jardin",
      title: "Jardin",
      description: "Aquí puedes plantar",
      image:
        "https://puntimmobiliari.com/wp-content/uploads/2021/03/casa-jardin.jpg",
    },
    exterior: {
      slug: "exterior",
      title: "Exterior",
      description: "Aquí es la calle",
      image:
        "https://inelba.com/wp-content/uploads/2021/08/iluminar-exterior-de-casa.jpg",
    },
  };
  return items[slug];
}
