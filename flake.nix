{
  description = "Example Python development environment for Zero to Nix";
  nixConfig = { 
    extra-substituters = "https://cuda-maintainers.cachix.org";
    extra-trusted-public-keys = "cuda-maintainers.cachix.org-1:0dq3bujKpuEPMCX6U4WylrUDZ9JyUG0VpVZa7CNfq5E=";
  };

  # Flake inputs
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs?ref=nixos-unstable";
  };

  # Flake outputs
  outputs = { self, nixpkgs }:
    let
      # Systems supported
      allSystems = [
        "x86_64-linux" # 64-bit Intel/AMD Linux
        "aarch64-linux" # 64-bit ARM Linux
        "x86_64-darwin" # 64-bit Intel macOS
        "aarch64-darwin" # 64-bit ARM macOS
      ];

      # Helper to provide system-specific attributes
      forAllSystems = f: nixpkgs.lib.genAttrs allSystems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
    in
    {
      # Development environment output
      devShells = forAllSystems ({ pkgs }: {
        default =
          let
            # Use Python 3.11
            python = pkgs.python311;
          in
          pkgs.mkShell {
            # The Nix packages provided in the environment
            packages = [
              pkgs.cudatoolkit
              pkgs.cudaPackages.cudnn
              pkgs.wget
              # Python plus helper tools
              (python.withPackages (ps: with ps; [
                numpy
                unidecode
                # pandas
                pyarrow
                scipy
                matplotlib
                tqdm
                opencv4
                torch-bin
                torchvision-bin
                ipykernel
                python-lsp-server
                jupyterlab
                jupyterlab-lsp
                jupyterlab-widgets
                ipywidgets
              ]))
            ];
            
            shellHook = ''
              exec fish
              # jupyter-lab
            '';
          };
      });
    };
}
