from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Character, Equipement
from django.contrib import messages

def post_list(request):
    characters = Character.objects.all()
    equipements = Equipement.objects.all()
    context = {
        "characters": characters,
        "equipements": equipements,
    }
    return render(request, 'blog/character_list.html', context)

 


def character_detail(request, id_character):
    character = get_object_or_404(Character, id_character=id_character)
    ancien_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
    lieu = character.lieu

    if request.method == "POST":
        form = MoveForm(request.POST, instance=character)

        if form.is_valid():
            nouveau_lieu = get_object_or_404(Equipement, id_equip=form.cleaned_data['lieu'].id_equip)

            # Zone de flottement est toujours libre
            if nouveau_lieu.id_equip == "Zone flottement":
                if character.etat == "Endormi":
                    ancien_lieu.disponibilite = "Libre"
                    ancien_lieu.save()
                    character.etat = "Affamé"
                    character.lieu = nouveau_lieu
                    ancien_lieu.save()
                    nouveau_lieu.save()
                    character.save()
                else:
                    messages.error(request, "Le changement n'est pas autorisé car l'état du personnage ne correspond pas.")
                    return redirect('character_detail', id_character=id_character)


            elif nouveau_lieu.disponibilite == "Libre":
                if nouveau_lieu.id_equip == "Distributeur de nourriture" and character.etat == "Affamé":
                    ancien_lieu.disponibilite = "Libre"
                    nouveau_lieu.disponibilite = "Occupé"
                    character.etat = "Repus"
                    character.lieu = nouveau_lieu
                    ancien_lieu.save()
                    nouveau_lieu.save()
                    character.save()


                elif nouveau_lieu.id_equip == "Récif ludique" and character.etat == "Repus":
                    ancien_lieu.disponibilite = "Libre"
                    nouveau_lieu.disponibilite = "Occupé"
                    character.etat = "Fatigué"
                    character.lieu = nouveau_lieu
                    ancien_lieu.save()
                    nouveau_lieu.save()
                    character.save()


                elif nouveau_lieu.id_equip == "Grotte aquatique" and character.etat == "Fatigué":
                    ancien_lieu.disponibilite = "Libre"
                    nouveau_lieu.disponibilite = "Occupé"
                    character.etat = "Endormi"
                    character.lieu = nouveau_lieu
                    ancien_lieu.save()
                    nouveau_lieu.save()
                    character.save()

                else:
                    messages.error(request, "Le changement n'est pas autorisé car l'état du personnage ne correspond pas.")
                    return redirect('character_detail', id_character=id_character)

            else:
                messages.error(request, "Le changement n'est pas autorisé car le lieu n'est pas libre.")
                return redirect('character_detail', id_character=id_character)

            return redirect('character_detail', id_character=id_character)

    else:
        form = MoveForm(instance=character)
        return render(request, 'blog/character_detail.html', {'character': character, 'lieu': lieu, 'form': form})

